from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json


app = FastAPI(title="Internal LLM Parser API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ollama configuration

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


# Request & Response Models

class ParseRequest(BaseModel):
    text: str


class ParseResponse(BaseModel):
    task: str
    active_window: dict | None
    exclusions: list



# System prompt (CRITICAL)

SYSTEM_PROMPT = """
You are an information extraction engine.

Return ONLY valid JSON.
No explanations.
No markdown.
No extra text.

Schema:
{
  "task": "hydration",
  "active_window": {
    "start": "HH:MM",
    "end": "HH:MM"
  } | null,
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

Rules:
- Use 24-hour format
- If something is missing, use null
- Do NOT invent times
"""

#API Endpoint
@app.post("/parse", response_model=ParseResponse)
def parse_schedule(req: ParseRequest):
    payload = {
        "model": MODEL,
        "prompt": f"{SYSTEM_PROMPT}\n\nUser input: {req.text}",
        "stream": False
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        r.raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=503, detail="LLM service unavailable")

    # Ollama returns  JSON
    try:
        output = r.json()["response"]
        parsed = json.loads(output)
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid LLM response")

    return parsed