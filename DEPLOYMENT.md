# Deployment

## Architecture

- **Frontend:** Netlify, publishing `dist/`
- **Backend:** Dockerized FastAPI service on Render (or another Docker-capable host)
- **Browser flow:** microphone → FastAPI → Whisper/VAD → LangGraph/RAG → browser TTS

## Backend: Render

This repository includes `render.yaml` and `Dockerfile`.

1. Create a Render account and choose **New → Blueprint**.
2. Select this GitHub repository.
3. Render reads `render.yaml` and builds the Docker image.
4. Wait for `/health` to report `{"status":"ok",...}`.
5. Copy the deployed backend URL, for example `https://enterprise-voice-ai-omniagent-api.onrender.com`.
6. Set `FRONTEND_URL` on the backend to the Netlify site URL after the frontend is deployed.

The first voice request may be slower because the `faster-whisper` model is downloaded/cached. The default deployment uses `WHISPER_MODEL=tiny` for a practical CPU demo.

## Frontend: Netlify

1. Create **Add new project → Import an existing project → GitHub**.
2. Select `kirankumarrout/enterprise-voice-ai-omniagent`.
3. Build command: `mkdir -p dist && cp -R static/. dist/`
4. Publish directory: `dist`
5. Add environment variable `BACKEND_URL` containing the deployed backend URL.
6. Deploy.

### Important API routing note

`static/index.html` currently uses relative `/api/...` URLs, so the Netlify site must proxy `/api/*` to the backend. After the backend URL is known, replace `__BACKEND_URL__` in `netlify.toml` with that URL before the final Netlify deployment, or configure the same proxy rule in Netlify's UI.

## Local verification

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000`.
