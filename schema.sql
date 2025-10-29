CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE patches (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    technique TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    patch_id INTEGER REFERENCES patches,
    user_id INTEGER REFERENCES users,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE patch_classes (
    id INTEGER PRIMARY KEY,
    patch_id INTEGER REFERENCES patches,
    title TEXT,
    value TEXT
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    patch_id INTEGER REFERENCES patches,
    image BLOB
);