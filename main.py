import re
import dateparser
import json
from datetime import datetime

def parse_time(text):
    parsed = dateparser.parse(text)
    return parsed.strftime("%H:%M") if parsed else None

def parse_input(user_text):
    result = {
        "task": "hydration",
        "active_window": {},
        "exclusions": []
    }

    # Matches times with or without colons: 9am, 9:00am, 1230pm, 12:30pm
    time_re = r'(\d{1,2}(:?\d{2})?\s*(am|pm)?)'

    # 1. Active Window 
    window_pattern = time_re + r'\s*(to|-\s*)\s*' + time_re
    window_match = re.search(window_pattern, user_text, re.I)

    if window_match:
        start = parse_time(window_match.group(1))
        end   = parse_time(window_match.group(5))
        result["active_window"] = {"start": start, "end": end}

    # 2. Lunch Matches 
    lunch_pattern = r'lunch.*?' + time_re + r'\s*(to|-\s*)\s*' + time_re
    lunch_match = re.search(lunch_pattern, user_text, re.I)
    if lunch_match:
        start = parse_time(lunch_match.group(1))
        end   = parse_time(lunch_match.group(5))
        result["exclusions"].append({"label": "lunch", "start": start, "end": end})

    # 3. Specific Breaks 
    break_keywords = ["coffee", "tea", "chai", "break", "pause", "rest", "snack", "sleep", "nap"]
    break_pattern = r'(' + '|'.join(break_keywords) + r').*?' + time_re
    break_matches = re.findall(break_pattern, user_text, re.I)

    for m in break_matches:
        time = parse_time(m[1])
        result["exclusions"].append({"label": "break", "time": time})

    # 4. Cleanup and Leftovers 
    all_times = re.findall(time_re, user_text, re.I)
    all_times_parsed = [parse_time(t[0]) for t in all_times]

    used_times = set()
    if result["active_window"]:
        used_times.update(filter(None, result["active_window"].values()))
    for ex in result["exclusions"]:
        used_times.update(filter(None, [ex.get("start"), ex.get("end"), ex.get("time")]))

    leftover = [t for t in all_times_parsed if t not in used_times]
    for t in leftover:
        result["exclusions"].append({"label": "break", "time": t})

    return result

def save_to_json(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"schedule_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"\n[SUCCESS] Data saved to {filename}")

if __name__ == "__main__":
    # --- RESTORED USER INSTRUCTIONS ---
    print("--- Hydration Scheduler Parser ---")
    print("Instructions:")
    print("1. Enter your work window (e.g., '9am to 5pm' or '0900 to 1700')")
    print("2. Mention lunch times (e.g., 'lunch 12:30pm to 1:45pm')")
    print("3. Add breaks (e.g., 'coffee at 3pm' or 'nap at 1400')")
    print("-" * 40)
    print("Example: 'working 9am to 3pm, lunch 1230pm to 145pm, break at 2pm'")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("User Schedule: ")

        if user_input.lower() in ['quit', 'exit', 'stop', 'q']:
            print("Exiting program. Stay hydrated!")
            break

        if not user_input.strip():
            continue

        parsed_data = parse_input(user_input)

        print("\nParsed JSON Output:")
        print(json.dumps(parsed_data, indent=4))

        save_to_json(parsed_data)

        # Re-prompting follow-up questions for the user
        print("\nFollow-up question: How frequently should I remind you to hydrate?")
        print("Do you have any other scheduling that you wish to add?")
        print("Do you wish to know how much water your body needs to maintain a healthy lifestyle?")
        print("-" * 40 + "\n")
        