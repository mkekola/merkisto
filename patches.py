import db

def add_patch(title, description, technique, user_id, classes):
    sql = "INSERT INTO patches (title, description, technique, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, technique, user_id])

    patch_id = db.last_insert_id()
    sql = "INSERT INTO patch_classes (patch_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [patch_id, title, value])

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

def update_patch(patch_id, title, description, technique):
    sql = "UPDATE patches SET title = ?, description = ?, technique = ? WHERE id = ?"
    db.execute(sql, [title, description, technique, patch_id])

def remove_patch(patch_id):
    sql = "DELETE FROM patches WHERE id = ?"
    db.execute(sql, [patch_id])

def find_patches(query):
    sql = """SELECT id, title
             FROM patches
             WHERE title LIKE ? OR
             description LIKE ?
             ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%"])
