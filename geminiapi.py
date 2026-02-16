import google.generativeai as genai
import json


genai.configure(api_key="AIzaSyCiFa8iwM-ec0DQEJA3nzeH8HkOC9jWnJA")
model = genai.GenerativeModel('gemini-1.5-flash')

def parse_with_gemini(user_text):
    prompt = f"""
    Extract hydration schedule details from this text: "{user_text}"
    Return ONLY a JSON object with this structure:
    {{
        "active_window": {{"start": "HH:MM", "end": "HH:MM"}},
        "exclusions": [{{ "label": "string", "start": "HH:MM", "end": "HH:MM", "time": "HH:MM" }}]
    }}
    If a field is unknown, use null. Use 24-hour format.
    """
    
    response = model.generate_content(prompt)
    # Strip any markdown formatting (like ```json) if present
    clean_json = response.text.strip().replace('```json', '').replace('```', '')
    return json.loads(clean_json)