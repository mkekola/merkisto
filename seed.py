import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM patches")
db.execute("DELETE FROM comments")
db.execute("DELETE FROM users")

user_count = 1000
patch_count = 10**5
comment_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])
    
for i in range(1, patch_count + 1):
    user_id = random.randint(1, user_count)
    db.execute("INSERT INTO patches (title, description, technique, user_id) VALUES (?, ?, ?, ?)",
               ["patch " + str(i),
                "Description for patch " + str(i),
                "Technique for patch " + str(i),
                user_id])
    
for i in range(1, comment_count + 1):
    patch_id = random.randint(1, patch_count)
    user_id = random.randint(1, user_count)
    db.execute("INSERT INTO comments (patch_id, user_id, content) VALUES (?, ?, ?)",
               [patch_id,
                user_id,
                "Comment " + str(i) + " for patch " + str(patch_id)])
    
db.commit()
db.close()
    