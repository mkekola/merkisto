import db

def add_patch(title, description, technique, user_id):
    sql = "INSERT INTO patches (title, description, technique, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, technique, user_id])

def get_all_patches():
    sql = "SELECT id, title FROM patches ORDER BY id DESC"

    return db.query(sql)

def get_patch(patch_id):
    sql = """SELECT patches.title,
                    patches.description,
                    patches.technique,
                    users.username
             FROM patches, users
             WHERE patches.user_id = users.id AND
                   patches.id = ?"""
    return db.query(sql, [patch_id])[0]