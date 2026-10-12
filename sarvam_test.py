
import os
from pathlib import Path
from sarvamai import SarvamAI

# Load the API key from .env
env_file = Path(__file__).with_name(".env")

for line in env_file.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line.startswith("SARVAM_API_KEY="):
        value = line.split("=", 1)[1].strip().strip('"').strip("'")
        if value:
            os.environ["SARVAM_API_KEY"] = value
        break

api_key = os.environ.get("SARVAM_API_KEY", "").strip()

if not api_key:
    raise SystemExit(
        "API key missing. Add your key to .env and try again."
    )

client = SarvamAI(api_subscription_key=api_key)

response = client.chat.completions(
    model="sarvam-105b-conversations",
    messages=[
        {
            "role": "user",
            "content": "Reply with: Sarvam API is working!"
        }
    ],
)

print(response.choices[0].message.content)
