import ollama
import json
from datetime import datetime

def parse_with_llm(user_text):
    model = "llama3"
    
    prompt = f"""
    You are a scheduling assistant. Extract hydration window and breaks from the text.
    Return ONLY a JSON object with this exact structure:
    {{
        "task": "hydration",
        "active_window": {{"start": "HH:MM", "end": "HH:MM"}},
        "exclusions": [
            {{"label": "lunch", "start": "HH:MM", "end": "HH:MM"}},
            {{"label": "break", "time": "HH:MM"}}
        ]
    }}
    Use 24-hour format (e.g., 13:00 for 1pm). If a value is missing, use null.
    
    User text: "{user_text}"
    """

    response = ollama.generate(model=model, prompt=prompt, format="json")
    return json.loads(response['response'])

def save_to_json(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"llm_schedule_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"\n[SUCCESS] Data saved to {filename}")

if __name__ == "__main__":
    print("Hydration Scheduler")
    while True:
        user_input = input("\nEnter your schedule (or 'q' to quit): ")
        if user_input.lower() in ['q', 'quit', 'exit']: break
        
        try:
            print("AI is thinking...")
            parsed_data = parse_with_llm(user_input)
            print("\nParsed JSON Output:")
            print(json.dumps(parsed_data, indent=4))
            save_to_json(parsed_data)
        except Exception as e:
            print(f"Error parsing input: {e}")