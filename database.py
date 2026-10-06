import sqlite3
import os

DB_PATH = "data/complaints.db"


def create_database():

    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            complaint TEXT,
            location TEXT,
            category TEXT,
            department TEXT,
            priority TEXT,
            severity TEXT,
            summary TEXT,
            status TEXT DEFAULT 'Pending',
            image_path TEXT
        )
    """)

    # Check existing columns
    cursor.execute("PRAGMA table_info(complaints)")
    columns = [column[1] for column in cursor.fetchall()]

    # Add name to old database
    if "name" not in columns:
        cursor.execute(
            "ALTER TABLE complaints ADD COLUMN name TEXT"
        )

    if "location" not in columns:
        cursor.execute(
            "ALTER TABLE complaints ADD COLUMN location TEXT"
        )

    if "category" not in columns:
        cursor.execute(
            "ALTER TABLE complaints ADD COLUMN category TEXT"
        )

    if "department" not in columns:
        cursor.execute(
            "ALTER TABLE complaints ADD COLUMN department TEXT"
        )

    if "priority" not in columns:
        cursor.execute(
            "ALTER TABLE complaints ADD COLUMN priority TEXT"
        )

    if "severity" not in columns:
        cursor.execute(
            "ALTER TABLE complaints ADD COLUMN severity TEXT"
        )

    if "summary" not in columns:
        cursor.execute(
            "ALTER TABLE complaints ADD COLUMN summary TEXT"
        )

    if "status" not in columns:
        cursor.execute(
            "ALTER TABLE complaints ADD COLUMN status TEXT DEFAULT 'Pending'"
        )

    if "image_path" not in columns:
        cursor.execute(
            "ALTER TABLE complaints ADD COLUMN image_path TEXT"
        )

    conn.commit()
    conn.close()


def add_complaint(
    name,
    complaint,
    location,
    category,
    department,
    priority,
    severity,
    summary,
    image_path
):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints
        (
            name,
            complaint,
            location,
            category,
            department,
            priority,
            severity,
            summary,
            status,
            image_path
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        complaint,
        location,
        category,
        department,
        priority,
        severity,
        summary,
        "Pending",
        image_path
    ))

    conn.commit()
    conn.close()


def get_complaints():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            complaint,
            location,
            category,
            department,
            priority,
            severity,
            summary,
            status,
            image_path
        FROM complaints
        ORDER BY id ASC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def update_status(complaint_id, new_status):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE complaints
        SET status = ?
        WHERE id = ?
    """, (
        new_status,
        complaint_id
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully!")