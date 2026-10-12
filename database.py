
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("healthcare.db")


def initialize_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT NOT NULL,
                reason TEXT NOT NULL,
                doctor TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Booked (demo)',
                UNIQUE (doctor, appointment_date, appointment_time)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS reminder_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                appointment_id INTEGER NOT NULL,
                reminder_date TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Preview only',
                FOREIGN KEY (appointment_id)
                    REFERENCES appointments(id),
                UNIQUE (appointment_id, reminder_date)
            )
        """)


def save_appointment(patient, slot):
    try:
        with sqlite3.connect(DB_PATH) as connection:
            connection.execute("""
                INSERT INTO appointments (
                    patient_name,
                    reason,
                    doctor,
                    appointment_date,
                    appointment_time
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                patient["name"],
                patient["reason"],
                slot["doctor"],
                slot["date"],
                slot["time"],
            ))
        return True

    except sqlite3.IntegrityError:
        return False


def get_booked_slots():
    with sqlite3.connect(DB_PATH) as connection:
        rows = connection.execute("""
            SELECT doctor, appointment_date, appointment_time
            FROM appointments
            WHERE status = 'Booked (demo)'
        """).fetchall()

    return set(rows)


def save_reminder_preview(appointment_id, reminder_date, message):
    try:
        with sqlite3.connect(DB_PATH) as connection:
            connection.execute("""
                INSERT INTO reminder_logs (
                    appointment_id, reminder_date, message
                )
                VALUES (?, ?, ?)
            """, (appointment_id, reminder_date, message))
        return True

    except sqlite3.IntegrityError:
        return False


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized: {DB_PATH}")
