import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)
    return classes

def add_patch(title, description, technique, user_id, classes):
    sql = "INSERT INTO patches (title, description, technique, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, technique, user_id])

    patch_id = db.last_insert_id()

    sql = "INSERT INTO patch_classes (patch_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [patch_id, class_title, class_value])
    return patch_id

def add_comment(patch_id, user_id, content):
    sql = "INSERT INTO comments (patch_id, user_id, content) VALUES (?, ?, ?)"
    db.execute(sql, [patch_id, user_id, content])

def add_image(patch_id, image):
    sql = "INSERT INTO images (patch_id, image) VALUES (?, ?)"
    db.execute(sql, [patch_id, image])

def get_image(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None

def get_images(patch_id):
    sql = "SELECT id FROM images WHERE patch_id = ?"
    return db.query(sql, [patch_id])

def remove_image(patch_id, image_id):
    sql = "DELETE FROM images WHERE id = ? AND patch_id = ?"
    db.execute(sql, [image_id, patch_id])

def get_comments(patch_id):
    sql = """SELECT comments.content,
                    comments.created_at,
                    users.id user_id,
                    users.username
             FROM comments, users
             WHERE comments.user_id = users.id AND
                   comments.patch_id = ?
             ORDER BY comments.created_at ASC"""
    return db.query(sql, [patch_id])

def get_classes(patch_id):
    sql = "SELECT title, value FROM patch_classes WHERE patch_id = ?"
    return db.query(sql, [patch_id])

def get_all_patches():
    sql = """SELECT patches.id, patches.title, users.id, users.username
             FROM patches, users
             WHERE patches.user_id = users.id
             ORDER BY patches.id DESC"""

    return db.query(sql)

def get_patch(patch_id):
    sql = """SELECT patches.id,
                    patches.title,
                    patches.description,
                    patches.technique,
                    users.id user_id,
                    users.username
             FROM patches, users
             WHERE patches.user_id = users.id AND
                   patches.id = ?"""
    result = db.query(sql, [patch_id])
    return result[0] if result else None

def update_patch(patch_id, title, description, technique, classes):
    sql = "UPDATE patches SET title = ?, description = ?, technique = ? WHERE id = ?"
    db.execute(sql, [title, description, technique, patch_id])

    sql = "DELETE FROM patch_classes WHERE patch_id = ?"
    db.execute(sql, [patch_id])

    sql = "INSERT INTO patch_classes (patch_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [patch_id, class_title, class_value])

def remove_patch(patch_id):
    sql = "DELETE FROM images WHERE patch_id = ?"
    db.execute(sql, [patch_id])
    sql = "DELETE FROM comments WHERE patch_id = ?"
    db.execute(sql, [patch_id])
    sql = "DELETE FROM patch_classes WHERE patch_id = ?"
    db.execute(sql, [patch_id])
    sql = "DELETE FROM patches WHERE id = ?"
    db.execute(sql, [patch_id])

def find_patches(query):
    sql = """SELECT id, title
             FROM patches
             WHERE title LIKE ? OR
             description LIKE ?
             ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%"])
