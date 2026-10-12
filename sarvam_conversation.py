
import os
from pathlib import Path

from sarvamai import SarvamAI


def load_api_key():
    env_file = Path(__file__).with_name(".env")

    if not env_file.exists():
        raise SystemExit("Missing .env file.")

    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if line.startswith("SARVAM_API_KEY="):
            value = line.split("=", 1)[1].strip().strip('"').strip("'")
            if value:
                os.environ["SARVAM_API_KEY"] = value
            break

    api_key = os.environ.get("SARVAM_API_KEY", "").strip()

    if not api_key:
        raise SystemExit("Add your API key to .env first.")

    return api_key


SYSTEM_PROMPT = """
You are the administrative assistant for a healthcare clinic.

Your responsibilities:
- Help patients with appointment-related enquiries.
- Collect only the minimum information needed for scheduling:
  appointment type, preferred date, and preferred time.
- Ask one clear follow-up question when information is missing.
- Be polite, concise, and easy to understand.
- Never diagnose, prescribe, or recommend medical treatment.
- Never claim that an appointment is booked or available.
  The Python application must verify availability and save
  the booking before confirming it.
- Do not request passwords, payment card details, or unnecessary
  medical information.
- If a patient describes an emergency, advise them to contact
  local emergency services or seek immediate medical care.
- This is a prototype. Encourage fictional information during tests.
"""


def main():
    client = SarvamAI(api_subscription_key=load_api_key())

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print("=== Sarvam Healthcare Assistant ===")
    print("Demo mode: use fictional information only.")
    print("Type 'quit' to exit.\n")

    while True:
        user_message = input("You: ").strip()

        if user_message.lower() in {"quit", "exit"}:
            print("Assistant: Goodbye!")
            break

        if not user_message:
            print("Please enter a message.")
            continue

        messages.append({
            "role": "user",
            "content": user_message,
        })

        try:
            response = client.chat.completions(
                model="sarvam-105b-conversations",
                messages=messages,
                max_tokens=300,
                reasoning_effort=None,
            )

            print("DEBUG: Response received.")
            print("DEBUG: Has choices:", bool(response.choices))
            if response.choices:
                print("DEBUG: Finish reason:", response.choices[0].finish_reason)
                print("DEBUG: Content type:", type(response.choices[0].message.content).__name__)
                print("DEBUG: Content is empty:", not response.choices[0].message.content)
            reply = response.choices[0].message.content

            if not reply:
                print("Assistant: I couldn't generate a reply. Please try again.")
                messages.pop()
                continue

            print(f"\nAssistant: {reply}\n")

            messages.append({
                "role": "assistant",
                "content": reply,
            })

        
        except Exception as exc:
            messages.pop()

            error_message = str(exc)
            api_key = os.environ.get("SARVAM_API_KEY", "")

            if api_key:
                error_message = error_message.replace(
                    api_key, "[REDACTED]"
                )

            print("\nRequest failed.")
            print(f"Error type: {type(exc).__name__}")
            print(f"Details: {error_message}\n")

if __name__ == "__main__":
    main()
