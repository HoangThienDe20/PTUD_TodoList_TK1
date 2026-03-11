# Hello To-Do — FastAPI minimal

Run locally:

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Endpoints:

- `GET /health` → { "status": "ok" }
- `GET /` → greeting message

Test with curl:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/
```

Open interactive docs: `http://127.0.0.1:8000/docs`
