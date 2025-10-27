import db

def add_patch(title, description, technique, user_id):
    sql = "INSERT INTO patches (title, description, technique, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, technique, user_id])

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
    return db.query(sql, [patch_id])[0]

def update_patch(patch_id, title, description, technique):
    sql = "UPDATE patches SET title = ?, description = ?, technique = ? WHERE id = ?"
    db.execute(sql, [title, description, technique, patch_id])

def remove_patch(patch_id):
    sql = "DELETE FROM patches WHERE id = ?"
    db.execute(sql, [patch_id])
