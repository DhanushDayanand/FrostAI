from google import genai
from google.genai import types
import json
from datetime import datetime

# Initialize the Gemini Client
client = genai.Client(api_key="AIzaSyCPDVWxWP13j5GWrPDvP29M7JPgsJSpOMc")

def parse_with_gemini(user_text):
    prompt = f"""
    Extract the hydration schedule from this text. 
    Return ONLY a JSON object with this structure:
    {{
        "task": "hydration",
        "active_window": {{"start": "HH:MM", "end": "HH:MM"}},
        "exclusions": [
            {{"label": "lunch", "start": "HH:MM", "end": "HH:MM"}},
            {{"label": "break", "time": "HH:MM"}}
        ]
    }}
    Use 24-hour format. User text: "{user_text}"
    """
    
    # We use Flash because it's fast and cheap for data parsing
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    return json.loads(response.text)

def save_to_json(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"gemini_schedule_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"\n[SUCCESS] Saved to {filename}")

if __name__ == "__main__":
    print("--- Gemini Hydration Scheduler ---")
    while True:
        user_input = input("\nEnter schedule: ")
        if user_input.lower() in ['q', 'quit']: break
        
        try:
            parsed_data = parse_with_gemini(user_input)
            print(json.dumps(parsed_data, indent=4))
            save_to_json(parsed_data)
        except Exception as e:
            print(f"Error: {e}")