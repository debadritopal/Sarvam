
from datetime import datetime

from database import (
    initialize_database,
    save_appointment,
    get_booked_slots,
)

# Demo appointment slots — synthetic data only.
AVAILABLE_SLOTS = [
    {"id": 1, "doctor": "Dr. Sharma", "date": "2026-10-14", "time": "10:00 AM"},
    {"id": 2, "doctor": "Dr. Sharma", "date": "2026-10-14", "time": "11:00 AM"},
    {"id": 3, "doctor": "Dr. Roy", "date": "2026-10-15", "time": "02:00 PM"},
]


def collect_patient_intake():
    print("\n=== Patient Intake ===")
    print("Demo mode: please use fictional information only.\n")

    patient = {
        "name": input("Patient name: ").strip(),
        "reason": input("Reason for visit (brief): ").strip(),
        "preferred_date": input("Preferred date (YYYY-MM-DD): ").strip(),
    }

    if not all(patient.values()):
        print("\nPlease fill in all fields.")
        return None

    try:
        datetime.strptime(patient["preferred_date"], "%Y-%m-%d")
    except ValueError:
        print("\nInvalid date format. Please use YYYY-MM-DD.")
        return None

    return patient


def show_available_slots():
    print("\n=== Available Appointments ===")
    booked_slots = get_booked_slots()

    available = [
        slot for slot in AVAILABLE_SLOTS
        if (slot["doctor"], slot["date"], slot["time"]) not in booked_slots
    ]

    if not available:
        print("No appointment slots are currently available.")
        return []

    for slot in available:
        print(
            f'{slot["id"]}. {slot["doctor"]} | '
            f'{slot["date"]} | {slot["time"]}'
        )

    return available


def book_appointment(patient):
    available = show_available_slots()

    matching_slots = [
        slot for slot in available
        if slot["date"] == patient["preferred_date"]
    ]

    if not matching_slots:
        print("\nNo slots match that date. Please try another date.")
        return None

    try:
        slot_id = int(input("\nEnter the appointment slot number: "))
    except ValueError:
        print("Please enter a valid slot number.")
        return None

    selected_slot = next(
        (slot for slot in matching_slots if slot["id"] == slot_id),
        None,
    )

    if selected_slot is None:
        print("Invalid or unavailable slot selection.")
        return None

    if not save_appointment(patient, selected_slot):
        print("That slot has already been booked. Please choose another.")
        return None

    appointment = {
        "patient_name": patient["name"],
        "reason": patient["reason"],
        "doctor": selected_slot["doctor"],
        "date": selected_slot["date"],
        "time": selected_slot["time"],
        "status": "Booked (demo)",
    }

    print("\n=== Appointment Confirmation ===")
    for key, value in appointment.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    print("\nAppointment saved to the local database (demo).")
    return appointment


def main():
    initialize_database()

    print("=" * 36)
    print(" HEALTHCARE OPERATIONS AGENT")
    print("=" * 36)

    patient = collect_patient_intake()

    if patient is None:
        return

    book_appointment(patient)


if __name__ == "__main__":
    main()
