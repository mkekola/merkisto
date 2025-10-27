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