/*
+-----------------------------------------------------------------------------+
[+] INFO
+-----------------------------------------------------------------------------+
 [Snake-Flask/src/snake_flask/access/schema.sql]

 Author      : Pascal Malouin (https://github.com/fantomH)
 Created     : 2026-07-14 19:32:13 UTC
 Updated     : 2026-07-14 19:32:13 UTC
 Description : Database schema for SnakeAccess.
+-----------------------------------------------------------------------------+
*/

/*
+-----------------------------------------------------------------------------+
[+] USERS
+-----------------------------------------------------------------------------+
*/

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 0,
    mfa_enabled INTEGER NOT NULL DEFAULT 0,
    mfa_secret TEXT,
    pin_enabled INTEGER NOT NULL DEFAULT 0,
    pin_secret TEXT
);
