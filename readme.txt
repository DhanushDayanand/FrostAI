Internal LLM Deployment

- Model: LLaMA 3 (8B)
- Runtime: Ollama
- Backend: FastAPI
- Data: Fully internal, no external API calls

How it works:
User → Web UI → Internal API → Local LLM → JSON response

Hardware:
- CPU: 12–16 vCPU recommended
- RAM: 32 GB
- GPU: Optional

Benefits:
- Zero per-request cost
- Full data privacy
- Vendor independent