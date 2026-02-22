from google import genai

client = genai.Client(api_key="AIzaSyCPDVWxWP13j5GWrPDvP29M7JPgsJSpOMc")
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents="Type 'Success' if you can read this."
    )
    print(response.text)
except Exception as e:
    print(f"Still failing: {e}")