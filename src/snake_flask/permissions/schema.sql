/*
+-----------------------------------------------------------------------------+
[+] INFO
+-----------------------------------------------------------------------------+
 [Snake-Flask/src/snake_flask/permissions/schema.sql]

 Author      : Pascal Malouin (https://github.com/fantomH)
 Created     : 2026-07-13 12:11:09 UTC
 Updated     : 2026-07-13 12:11:09 UTC
 Description : Database schema for SnakePermissions.
+-----------------------------------------------------------------------------+
*/

/*
+-----------------------------------------------------------------------------+
[+] PERMISSIONS
+-----------------------------------------------------------------------------+
*/

CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT ''
);


/*
+-----------------------------------------------------------------------------+
[+] ROLES
+-----------------------------------------------------------------------------+
*/

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT ''
);


/*
+-----------------------------------------------------------------------------+
[+] PERMISSION SETS
+-----------------------------------------------------------------------------+
*/

CREATE TABLE IF NOT EXISTS permission_sets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL DEFAULT ''
);


/*
+-----------------------------------------------------------------------------+
[+] USER -> ROLE
+-----------------------------------------------------------------------------+
*/

CREATE TABLE IF NOT EXISTS user_roles (
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,

    PRIMARY KEY (user_id, role_id),

    FOREIGN KEY (role_id)
        REFERENCES roles(id)
        ON DELETE CASCADE
);

/*
+-----------------------------------------------------------------------------+
[+] USER -> DIRECT PERMISSION
+-----------------------------------------------------------------------------+
*/

CREATE TABLE IF NOT EXISTS user_direct_permissions (
    user_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,

    PRIMARY KEY (user_id, permission_id),

    FOREIGN KEY (permission_id)
        REFERENCES permissions(id)
        ON DELETE CASCADE
);

/*
+-----------------------------------------------------------------------------+
[+] USER -> PERMISSION SET
+-----------------------------------------------------------------------------+
*/

CREATE TABLE IF NOT EXISTS user_permission_sets (
    user_id INTEGER NOT NULL,
    permission_set_id INTEGER NOT NULL,

    PRIMARY KEY (user_id, permission_set_id),

    FOREIGN KEY (permission_set_id)
        REFERENCES permission_sets(id)
        ON DELETE CASCADE
);

/*
+-----------------------------------------------------------------------------+
[+] ROLE -> DIRECT PERMISSION
+-----------------------------------------------------------------------------+
*/

CREATE TABLE IF NOT EXISTS role_direct_permissions (
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,

    PRIMARY KEY (role_id, permission_id),

    FOREIGN KEY (role_id)
        REFERENCES roles(id)
        ON DELETE CASCADE,

    FOREIGN KEY (permission_id)
        REFERENCES permissions(id)
        ON DELETE CASCADE
);

/*
+-----------------------------------------------------------------------------+
[+] ROLE -> PERMISSION SET
+-----------------------------------------------------------------------------+
*/

CREATE TABLE IF NOT EXISTS role_permission_sets (
    role_id INTEGER NOT NULL,
    permission_set_id INTEGER NOT NULL,

    PRIMARY KEY (role_id, permission_set_id),

    FOREIGN KEY (role_id)
        REFERENCES roles(id)
        ON DELETE CASCADE,

    FOREIGN KEY (permission_set_id)
        REFERENCES permission_sets(id)
        ON DELETE CASCADE
);

/*
+-----------------------------------------------------------------------------+
[+] PERMISSION SET -> PERMISSION
+-----------------------------------------------------------------------------+
*/

CREATE TABLE IF NOT EXISTS permission_set_permissions (
    permission_set_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,

    PRIMARY KEY (permission_set_id, permission_id),

    FOREIGN KEY (permission_set_id)
        REFERENCES permission_sets(id)
        ON DELETE CASCADE,

    FOREIGN KEY (permission_id)
        REFERENCES permissions(id)
        ON DELETE CASCADE
);

/*
+-----------------------------------------------------------------------------+
[+] INDEXES
+-----------------------------------------------------------------------------+
*/

CREATE INDEX IF NOT EXISTS idx_user_roles_user_id
    ON user_roles(user_id);

CREATE INDEX IF NOT EXISTS idx_user_roles_role_id
    ON user_roles(role_id);

CREATE INDEX IF NOT EXISTS idx_user_direct_permissions_user_id
    ON user_direct_permissions(user_id);

CREATE INDEX IF NOT EXISTS idx_user_direct_permissions_permission_id
    ON user_direct_permissions(permission_id);

CREATE INDEX IF NOT EXISTS idx_user_permission_sets_user_id
    ON user_permission_sets(user_id);

CREATE INDEX IF NOT EXISTS idx_user_permission_sets_permission_set_id
    ON user_permission_sets(permission_set_id);

CREATE INDEX IF NOT EXISTS idx_role_direct_permissions_role_id
    ON role_direct_permissions(role_id);

CREATE INDEX IF NOT EXISTS idx_role_direct_permissions_permission_id
    ON role_direct_permissions(permission_id);

CREATE INDEX IF NOT EXISTS idx_role_permission_sets_role_id
    ON role_permission_sets(role_id);

CREATE INDEX IF NOT EXISTS idx_role_permission_sets_permission_set_id
    ON role_permission_sets(permission_set_id);

CREATE INDEX IF NOT EXISTS idx_permission_set_permissions_permission_set_id
    ON permission_set_permissions(permission_set_id);

CREATE INDEX IF NOT EXISTS idx_permission_set_permissions_permission_id
    ON permission_set_permissions(permission_id);
