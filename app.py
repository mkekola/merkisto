import secrets
import sqlite3
from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session
import markupsafe
import config
import db
import patches
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br/>")
    return markupsafe.Markup(content)


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
    comments = patches.get_comments(patch_id)
    images = patches.get_images(patch_id)
    return render_template("show_patch.html", patch=patch, classes=classes, comments=comments, images=images)

@app.route("/new_patch")
def new_patch():
    require_login()
    classes = patches.get_all_classes()
    return render_template("new_patch.html", classes=classes)

@app.route("/create_comment/<int:patch_id>", methods=["POST"])
def create_comment(patch_id):
    require_login()
    check_csrf()

    content = request.form["comment"]
    if not content or len(content) > 300:
        abort(403)
    user_id = session["user_id"]

    patches.add_comment(patch_id, user_id, content)
    flash("Kommentti lisätty onnistuneesti.")

    return redirect("/patch/" + str(patch_id))

@app.route("/create_patch", methods=["POST"])
def create_patch():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 50:
        flash("Virhe: Otsikon on oltava 1-50 merkkiä pitkä.")
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 500:
        flash("Virhe: Kuvauksen on oltava 1-500 merkkiä pitkä.")
        abort(403)
    technique = request.form["technique"]
    if not technique:
        flash("Virhe: Tekniikan on oltava valittuna.")
        abort(403)
    user_id = session["user_id"]

    all_classes = patches.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            if parts[0] not in all_classes:
                flash("Virhe: Kategoriaa ei löytynyt.")
                abort(403)
            if parts[1] not in all_classes[parts[0]]:
                flash("Virhe: Lähdettä ei löytynyt.")
                abort(403)
            classes.append((parts[0], parts[1]))

    patch_id = patches.add_patch(title, description, technique, user_id, classes)
    return redirect("/patch/" + str(patch_id))

@app.route("/edit_patch/<int:patch_id>")
def edit_patch(patch_id):
    require_login()
    patch = patches.get_patch(patch_id)
    if not patch:
        flash("Virhe: Merkkiä ei löytynyt.")
        abort(404)
    if patch["user_id"] != session.get("user_id"):
        flash("Virhe: Sinulla ei ole oikeuksia muokata tätä merkkiä.")
        abort(403)

    all_classes = patches.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in patches.get_classes(patch_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_patch.html", patch=patch, all_classes=all_classes, classes=classes)

@app.route("/images/<int:patch_id>")
def edit_images(patch_id):
    require_login()
    patch = patches.get_patch(patch_id)
    if not patch:
        flash("Virhe: Merkkiä ei löytynyt.")
        abort(404)
    if patch["user_id"] != session.get("user_id"):
        flash("Virhe: Sinulla ei ole oikeuksia muokata tätä merkkiä.")
        abort(403)

    images = patches.get_images(patch_id)

    return render_template("images.html", patch=patch, images=images)

@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()
    check_csrf()

    patch_id = request.form["patch_id"]
    patch = patches.get_patch(patch_id)
    if not patch:
        flash("Virhe: Merkkiä ei löytynyt.")
        abort(404)
    if patch["user_id"] != session.get("user_id"):
        flash("Virhe: Sinulla ei ole oikeuksia muokata tätä merkkiä.")
        abort(403)

    file = request.files["image"]
    if not file.filename.endswith(".png"):
        return "VIRHE: vain .png kuvat sallittu"

    image = file.read()
    if len(image) > 2 * 1024 * 1024:
        flash("Virhe: kuvan koko enintään 2MB")
        return redirect("/images/" + str(patch_id))

    patches.add_image(patch_id, image)

    return redirect("/images/" + str(patch_id))

@app.route("/remove_images", methods=["POST"])
def remove_images():
    require_login()
    check_csrf()

    patch_id = request.form["patch_id"]
    patch = patches.get_patch(patch_id)
    if not patch:
        flash("Virhe: Merkkiä ei löytynyt.")
        abort(404)
    if patch["user_id"] != session.get("user_id"):
        flash("Virhe: Sinulla ei ole oikeuksia muokata tätä merkkiä.")
        abort(403)

    for image_id in request.form.getlist("image_id"):
        patches.remove_image(patch_id, image_id)

    return redirect("/images/" + str(patch_id))

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = patches.get_image(image_id)
    if not image:
        flash("Virhe: Kuvaa ei löytynyt.")
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/png")
    return response

@app.route("/update_patch/<int:patch_id>", methods=["POST"])
def update_patch(patch_id):
    require_login()
    check_csrf()

    patch = patches.get_patch(patch_id)
    if not patch:
        flash("Virhe: Merkkiä ei löytynyt.")
        abort(404)
    if patch["user_id"] != session["user_id"]:
        flash("Virhe: Sinulla ei ole oikeuksia muokata tätä merkkiä.")
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 50:
        flash("Virhe: Otsikon on oltava 1-50 merkkiä pitkä.")
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 500:
        flash("Virhe: Kuvauksen on oltava 1-500 merkkiä pitkä.")
        abort(403)
    technique = request.form["technique"]
    if not technique:
        flash("Virhe: Tekniikan on oltava valittuna.")
        abort(403)

    all_classes = patches.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                flash("Virhe: Kategoriaa ei löytynyt.")
                abort(403)
            if class_value not in all_classes[class_title]:
                flash("Virhe: Lähdettä ei löytynyt.")
                abort(403)
            classes.append((class_title, class_value))

    patches.update_patch(patch_id, title, description, technique, classes)

    return redirect("/patch/" + str(patch_id))

@app.route("/remove_patch/<int:patch_id>", methods=["GET", "POST"])
def remove_patch(patch_id):
    require_login()

    patch = patches.get_patch(patch_id)
    if not patch:
        flash("Virhe: Merkkiä ei löytynyt.")
        abort(404)
    if patch["user_id"] != session.get("user_id"):
        flash("Virhe: Sinulla ei ole oikeuksia muokata tätä merkkiä.")
        abort(403)
    if request.method == "POST":
        check_csrf()
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
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana" + redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")


