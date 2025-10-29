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

def get_classes(patch_id):
    sql = "SELECT title, value FROM patch_classes WHERE patch_id = ?"
    return db.query(sql, [patch_id])

def get_all_patches():
    sql = "SELECT id, title FROM patches ORDER BY id DESC"

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
