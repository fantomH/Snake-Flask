-- [+] -------------------------------------------------------------------| INFO
-- [snake_permissions/schema.sql]
-- description : Database schema for Snake-Permissions.

CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS user_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS permission_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS user_group_members (
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,

    PRIMARY KEY (user_id, group_id),

    FOREIGN KEY (group_id)
        REFERENCES user_groups(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_permissions (
    user_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,

    PRIMARY KEY (user_id, permission_id),

    FOREIGN KEY (permission_id)
        REFERENCES permissions(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_group_permissions (
    group_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,

    PRIMARY KEY (group_id, permission_id),

    FOREIGN KEY (group_id)
        REFERENCES user_groups(id)
        ON DELETE CASCADE,

    FOREIGN KEY (permission_id)
        REFERENCES permissions(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS permission_group_permissions (
    permission_group_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,

    PRIMARY KEY (permission_group_id, permission_id),

    FOREIGN KEY (permission_group_id)
        REFERENCES permission_groups(id)
        ON DELETE CASCADE,

    FOREIGN KEY (permission_id)
        REFERENCES permissions(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_permission_groups (
    user_id INTEGER NOT NULL,
    permission_group_id INTEGER NOT NULL,

    PRIMARY KEY (user_id, permission_group_id),

    FOREIGN KEY (permission_group_id)
        REFERENCES permission_groups(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_group_permission_groups (
    group_id INTEGER NOT NULL,
    permission_group_id INTEGER NOT NULL,

    PRIMARY KEY (group_id, permission_group_id),

    FOREIGN KEY (group_id)
        REFERENCES user_groups(id)
        ON DELETE CASCADE,

    FOREIGN KEY (permission_group_id)
        REFERENCES permission_groups(id)
        ON DELETE CASCADE
);
