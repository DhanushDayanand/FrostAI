import json
from datetime import datetime
from openai import OpenAI

client = OpenAI()


SYSTEM_PROMPT = """
You are a scheduling assistant.

Extract hydration scheduling information from user input.

Rules:
- Always return VALID JSON
- Use 24-hour time format (HH:MM)
- If a field is missing, use null
- Follow this schema exactly

Schema:
{
  "task": "hydration",
  "active_window": {
    "start": "HH:MM",
    "end": "HH:MM"
  },
  "exclusions": [
    {
      "label": "string",
      "start": "HH:MM",
      "end": "HH:MM"
    },
    {
      "label": "string",
      "time": "HH:MM"
    }
  ]
}
"""


def parse_with_chatgpt(user_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        temperature=0
    )

    content = response.choices[0].message.content
    return json.loads(content)


def save_to_json(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"schedule_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\n[SUCCESS] Data saved to {filename}")


if __name__ == "__main__":
    print("--- Hydration Scheduler (ChatGPT Powered) ---")
    print("Example:")
    print("working 9am to 5pm, lunch 12:30pm to 1:30pm, coffee at 4pm")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("User Schedule: ").strip()

        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting. Stay hydrated 💧")
            break

        if not user_input:
            continue

        try:
            parsed_data = parse_with_chatgpt(user_input)

            print("\nParsed JSON Output:")
            print(json.dumps(parsed_data, indent=4))

            save_to_json(parsed_data)

        except Exception as e:
            print("❌ Error parsing input:", e)

        print("-" * 40)
