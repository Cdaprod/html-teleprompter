"""FastAPI workspace API smoke tests."""
import importlib
import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient


def load_app(tmp_path: Path):
    os.environ["TELEPROMPTER_PROJECTS_ROOT"] = str(tmp_path)
    if "app.main" in sys.modules:
        importlib.reload(sys.modules["app.main"])
    main = importlib.import_module("app.main")
    return TestClient(main.app)


def test_project_script_and_export(tmp_path):
    client = load_app(tmp_path)

    assert client.get("/health").json()["status"] == "ok"

    create_project = client.post("/api/projects", json={"name": "demo"})
    assert create_project.status_code == 200

    script_payload = {"title": "Example Run", "content": "Hello teleprompter", "format": "md"}
    created = client.post("/api/projects/demo/scripts", json=script_payload).json()
    script_name = created["name"]

    listed = client.get("/api/projects/demo/scripts").json()["scripts"]
    assert script_name in listed

    fetched = client.get(f"/api/projects/demo/scripts/{script_name}").json()
    assert "Hello teleprompter" in fetched["content"]

    updated = client.put(
        f"/api/projects/demo/scripts/{script_name}",
        json={"title": "Example Run", "content": "Updated body", "format": "md"},
    )
    assert updated.status_code == 200

    export_resp = client.post(f"/api/projects/demo/scripts/{script_name}/export").json()["exports"]
    assert Path(export_resp["text"]).exists()
    assert Path(export_resp["prompt"]).exists()

    run_payload = {
        "script": script_name,
        "take_id": "take-1",
        "started_at": "2024-01-01T00:00:00Z",
        "ended_at": "2024-01-01T00:05:00Z",
        "speed_events": [],
        "markers": [],
        "notes": "initial run",
    }
    run_resp = client.post("/api/projects/demo/runs", json=run_payload)
    assert run_resp.status_code == 200
    assert Path(run_resp.json()["path"]).exists()

    projects = client.get("/api/projects").json()["projects"]
    assert "demo" in projects
