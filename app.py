import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import db
import patches
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_patches = patches.get_all_patches()
    return render_template("index.html", patches=all_patches)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    patches = users.get_patches(user_id)
    return render_template("show_user.html", user=user, patches=patches)

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
    classes = patches.get_classes(patch_id)
    return render_template("show_patch.html", patch=patch, classes=classes)

@app.route("/new_patch")
def new_patch():
    require_login()
    classes = patches.get_all_classes()
    return render_template("new_patch.html", classes=classes)

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

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            classes.append((parts[0], parts[1]))
            
    patches.add_patch(title, description, technique, user_id, classes)

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

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: käyttäjätunnus on jo olemassa" + redirect("/register")

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana" + redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")


