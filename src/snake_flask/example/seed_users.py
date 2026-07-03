import random
import sqlite3

from werkzeug.security import generate_password_hash


DB = "instance/data.sqlite"

FIRST_NAMES = [
    "John", "Jane", "Mike", "Sarah", "David", "Emily",
    "Chris", "Jessica", "Daniel", "Laura", "Kevin", "Anna",
    "Marc", "Julie", "Alex", "Sophie", "Nathan", "Olivia",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Miller", "Davis", "Wilson", "Moore", "Taylor",
    "Anderson", "Thomas", "Jackson", "White", "Martin",
    "Lee", "Clark", "Walker",
]

conn = sqlite3.connect(DB)

for i in range(1, 1001):

    firstname = random.choice(FIRST_NAMES)
    lastname = random.choice(LAST_NAMES)

    username = f"{firstname.lower()}.{lastname.lower()}{i}"
    email = f"{username}@example.test"

    conn.execute("""
        INSERT OR IGNORE INTO users (
            username,
            firstname,
            lastname,
            email,
            password_hash,
            is_active
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        username,
        firstname,
        lastname,
        email,
        generate_password_hash("password"),
        1 if i % 3 else 0,
    ))

conn.commit()
conn.close()

print("Inserted 1000 users")
