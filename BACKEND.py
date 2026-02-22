from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json

app = FastAPI(title="Internal LLM Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

class ParseRequest(BaseModel):
    text: str

SYSTEM_PROMPT = """
You are an internal scheduling parser.

Return ONLY valid JSON.
No explanation.
No markdown.

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
- 24-hour format
- Do not guess times
- Missing values → null
"""

@app.post("/parse")
def parse(req: ParseRequest):
    payload = {
        "model": MODEL,
        "prompt": SYSTEM_PROMPT + "\nUser input: " + req.text,
        "stream": False
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=60)
        r.raise_for_status()
        output = r.json()["response"]
        return json.loads(output)
    except Exception:
        raise HTTPException(status_code=500, detail="LLM parsing failed")