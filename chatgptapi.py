import os
import json
from datetime import datetime
from openai import OpenAI



MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)



def parse_input_with_chatgpt(user_text):
    """
    Sends user input to ChatGPT and expects structured JSON output
    for hydration scheduling.
    """

    system_prompt = """
You are a scheduling parser.

Extract hydration schedule information from the user's message.

Return ONLY valid JSON in the following exact structure:

{
  "task": "hydration",
  "active_window": {
    "start": "HH:MM",
    "end": "HH:MM"
  },
  "exclusions": [
    {
      "label": "lunch",
      "start": "HH:MM",
      "end": "HH:MM"
    },
    {
      "label": "break",
      "time": "HH:MM"
    }
  ]
}

Rules:
- Use 24-hour time format
- If a field is unknown, use null
- Do not add explanations or extra keys
- Output JSON only
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ]
        )

        raw_output = response.choices[0].message.content
        return json.loads(raw_output)

    except json.JSONDecodeError:
        print("[ERROR] ChatGPT returned invalid JSON.")
        return None

    except Exception as e:
        print(f"[ERROR] ChatGPT API failed: {e}")
        return None




def save_to_json(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"schedule_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\n[SUCCESS] Data saved to {filename}")




if __name__ == "__main__":

    print("\n--- Hydration Scheduler (ChatGPT Powered) ---")
    print("Instructions:")
    print("• Enter your working hours")
    print("• Mention lunch or breaks naturally")
    print("• Example:")
    print("  'Working 9am to 5pm, lunch 1 to 2, coffee at 4'")
    print("Type 'exit' or 'quit' to stop.")
    print("-" * 50)

    while True:
        user_input = input("\nUser Schedule: ").strip()

        if user_input.lower() in ["exit", "quit", "q", "stop"]:
            print("Exiting program. Stay hydrated! 💧")
            break

        if not user_input:
            continue

        parsed_data = parse_input_with_chatgpt(user_input)

        if not parsed_data:
            print("[WARNING] Could not parse schedule. Try again.")
            continue

        print("\nParsed JSON Output:")
        print(json.dumps(parsed_data, indent=4))

        save_to_json(parsed_data)

        print("\nFollow-up questions:")
        print("• How frequently should I remind you to hydrate?")
        print("• Do you have any other schedule constraints?")
        print("• Would you like water intake recommendations?")
        print("-" * 50)
