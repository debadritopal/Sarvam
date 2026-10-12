
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

from database import DB_PATH, initialize_database, save_reminder_preview


def get_upcoming_appointments():
    today = date.today()
    end_date = today + timedelta(days=7)

    with sqlite3.connect(DB_PATH) as connection:
        rows = connection.execute("""
            SELECT id, patient_name, doctor, appointment_date,
                   appointment_time
            FROM appointments
            WHERE appointment_date BETWEEN ? AND ?
              AND status = 'Booked (demo)'
            ORDER BY appointment_date, appointment_time
        """, (today.isoformat(), end_date.isoformat())).fetchall()

    return rows


def main():
    initialize_database()

    print("=== Appointment Reminder Preview ===")
    print("Demo mode: no messages will be sent.\n")

    appointments = get_upcoming_appointments()

    if not appointments:
        print("No appointments found in the next 7 days.")
        return

    today = date.today().isoformat()

    for appointment_id, patient, doctor, appt_date, appt_time in appointments:
        appointment_day = datetime.strptime(
            appt_date, "%Y-%m-%d"
        ).strftime("%d %B %Y")

        message = (
            f"Hello {patient}, this is a reminder of your "
            f"appointment with {doctor} on {appointment_day} "
            f"at {appt_time}. Please contact the clinic if "
            "you need to reschedule."
        )

        saved = save_reminder_preview(
            appointment_id, today, message
        )

        if saved:
            print("-" * 40)
            print(message)
            print("Status: Preview recorded (not sent)")
        else:
            print(
                f"Reminder already recorded for appointment "
                f"#{appointment_id} today; skipping."
            )


if __name__ == "__main__":
    main()
