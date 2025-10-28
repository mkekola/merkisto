import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import patches

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_patches = patches.get_all_patches()
    return render_template("index.html", patches=all_patches)

@app.route("/find_patch", methods=["GET", "POST"])
def find_patch():
    query = request.args.get("query")
    if query:
        results = patches.find_patches(query)
    else:
        query = ""
        results = []
    return render_template("find_patch.html", query=query, patches=results)

@app.route("/patch/<int:patch_id>")
def show_patch(patch_id):
    patch = patches.get_patch(patch_id)
    if not patch:
        abort(404)
    return render_template("show_patch.html", patch=patch)

@app.route("/new_patch")
def new_patch():
    require_login()
    return render_template("new_patch.html")

@app.route("/create_patch", methods=["POST"])
def create_patch():
    require_login()
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 500:
        abort(403)
    technique = request.form["technique"]
    if not technique:
        abort(403)
    user_id = session["user_id"]

    patches.add_patch(title, description, technique, user_id)

    return redirect("/")

@app.route("/edit_patch/<int:patch_id>")
def edit_patch(patch_id):
    require_login()
    patch = patches.get_patch(patch_id)
    if not patch:
        abort(404)
    if patch["user_id"] != session.get("user_id"):
        abort(403)
    return render_template("edit_patch.html", patch=patch)

@app.route("/update_patch/<int:patch_id>", methods=["POST"])
def update_patch(patch_id):
    require_login()
    patch = patches.get_patch(patch_id)
    if not patch:
        abort(404)
    if patch["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 500:
        abort(403)
    technique = request.form["technique"]
    if not technique:
        abort(403)

    patches.update_patch(patch_id, title, description, technique)

    return redirect("/patch/" + str(patch_id))

@app.route("/remove_patch/<int:patch_id>", methods=["GET", "POST"])
def remove_patch(patch_id):
    require_login()
    patch = patches.get_patch(patch_id)
    if not patch:
        abort(404)
    if patch["user_id"] != session.get("user_id"):
        abort(403)
    if request.method == "POST":
        if "remove" in request.form:
            patches.remove_patch(patch_id)
            return redirect("/")
        elif "back" in request.form:
            return redirect("/patch/" + str(patch_id))
    return render_template("remove_patch.html", patch=patch)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

    if check_password_hash(password_hash, password):
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")


