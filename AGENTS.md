# Agent Guidelines

- Static assets now live under `public/` so UI changes should target that directory; keep `docs/` adjacent to `public/index.html`.
- The FastAPI server is defined in `app/main.py` and exposes the workspace API; prefer extending it rather than adding new servers.
- Use `/api/docs/list` to regenerate `public/docs/list.json` when transcript files change.
- Tests include Node integrity checks (`tests/teleprompter.test.js`) and FastAPI smoke tests (`tests/test_api.py`). Update both when adjusting UI or API contracts.
- Docker tooling lives in `docker/` with the root `docker-compose.yaml` using Compose `include:`. Keep dev commands copy-pastable in the README when workflows change.
