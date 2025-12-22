"""FastAPI dev server for the HTML teleprompter workspace.

Usage:
    uvicorn app.main:app --host ${TELEPROMPTER_HOST:-0.0.0.0} --port ${TELEPROMPTER_PORT:-8790} --reload
"""
from __future__ import annotations

import json
import os
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional

from fastapi import Body, FastAPI, HTTPException, Path as FastAPIPath
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


def _get_projects_root() -> Path:
    root = Path(os.getenv("TELEPROMPTER_PROJECTS_ROOT", "/data/projects")).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    return root


PROJECTS_ROOT: Path = _get_projects_root()
PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"
INDEX_FILE = PUBLIC_DIR / "index.html"


class ProjectCreate(BaseModel):
    name: str = Field(..., description="Project folder name")


class ScriptCreate(BaseModel):
    title: str = Field(..., description="Human-friendly title for the script")
    content: str = Field(..., description="Script body in plain text or markdown")
    format: str = Field(..., regex="^(md|txt)$", description="File extension to use for the script")


class RunRecord(BaseModel):
    script: str = Field(..., description="Script filename used for the take")
    take_id: str = Field(..., description="External or generated take identifier")
    started_at: str = Field(..., description="ISO timestamp when the take began")
    ended_at: str = Field(..., description="ISO timestamp when the take ended")
    speed_events: List[dict] = Field(default_factory=list, description="Recorded speed change events")
    markers: List[dict] = Field(default_factory=list, description="Markers added during the take")
    notes: Optional[str] = Field(default=None, description="Freeform notes for the take")


app = FastAPI(title="Teleprompter Workspace Service")


def _allowed_name(value: str) -> bool:
    return value and "/" not in value and ".." not in value and value.strip() == value


def _project_path(project: str) -> Path:
    if not _allowed_name(project):
        raise HTTPException(status_code=400, detail="Invalid project name")
    return PROJECTS_ROOT / project


def _teleprompter_dir(project: str) -> Path:
    project_dir = _project_path(project)
    return project_dir / "teleprompter"


def _ensure_project_structure(project: str) -> Path:
    project_dir = _project_path(project)
    teleprompter_dir = project_dir / "teleprompter"
    scripts_dir = teleprompter_dir / "scripts"
    runs_dir = teleprompter_dir / "runs"
    exports_dir = teleprompter_dir / "exports"

    for directory in (project_dir, teleprompter_dir, scripts_dir, runs_dir, exports_dir):
        directory.mkdir(parents=True, exist_ok=True)

    index_json = teleprompter_dir / "index.json"
    if not index_json.exists():
        index_json.write_text(
            json.dumps(
                {
                    "project": project,
                    "created_at": datetime.utcnow().isoformat(),
                    "scripts_dir": str(scripts_dir),
                    "runs_dir": str(runs_dir),
                    "exports_dir": str(exports_dir),
                },
                indent=2,
            )
        )

    return teleprompter_dir


def _slugify(title: str) -> str:
    safe = "".join(ch if ch.isalnum() else "-" for ch in title.lower())
    safe = "-".join(filter(None, safe.split("-")))
    return safe or "script"


def _script_path(project: str, script_name: str) -> Path:
    if not _allowed_name(script_name):
        raise HTTPException(status_code=400, detail="Invalid script name")
    scripts_dir = _teleprompter_dir(project) / "scripts"
    target = (scripts_dir / script_name).resolve()
    if scripts_dir.resolve() not in target.parents and scripts_dir.resolve() != target.parent:
        raise HTTPException(status_code=400, detail="Script path traversal blocked")
    return target


origins = os.getenv("TELEPROMPTER_CORS_ORIGINS", "*")
allow_all = origins == "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all else [o.strip() for o in origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"] if allow_all else ["GET", "POST", "PUT", "OPTIONS"],
    allow_headers=["*"] if allow_all else ["Content-Type", "Authorization"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/projects")
def list_projects() -> dict:
    projects = [p.name for p in PROJECTS_ROOT.iterdir() if p.is_dir()]
    return {"projects": sorted(projects)}


@app.post("/api/projects")
def create_project(payload: ProjectCreate = Body(...)) -> dict:
    teleprompter_dir = _ensure_project_structure(payload.name)
    return {"name": payload.name, "path": str(teleprompter_dir)}


@app.get("/api/projects/{project}/scripts")
def list_scripts(project: str = FastAPIPath(...)) -> dict:
    scripts_dir = _teleprompter_dir(project) / "scripts"
    if not scripts_dir.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    scripts = [p.name for p in scripts_dir.iterdir() if p.is_file()]
    return {"scripts": sorted(scripts)}


@app.post("/api/projects/{project}/scripts")
def create_script(
    project: str = FastAPIPath(...),
    payload: ScriptCreate = Body(...),
) -> dict:
    teleprompter_dir = _ensure_project_structure(project)
    scripts_dir = teleprompter_dir / "scripts"
    slug = _slugify(payload.title)
    filename = f"{slug}__{date.today().isoformat()}__v1.{payload.format}"
    path = scripts_dir / filename
    path.write_text(payload.content)
    return {"name": filename, "path": str(path)}


@app.get("/api/projects/{project}/scripts/{script_name}")
def read_script(
    project: str = FastAPIPath(...),
    script_name: str = FastAPIPath(...),
) -> dict:
    path = _script_path(project, script_name)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Script not found")
    return {"name": script_name, "content": path.read_text()}


@app.put("/api/projects/{project}/scripts/{script_name}")
def update_script(
    project: str = FastAPIPath(...),
    script_name: str = FastAPIPath(...),
    payload: ScriptCreate = Body(...),
) -> dict:
    path = _script_path(project, script_name)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Script not found")

    temp_path = path.with_suffix(path.suffix + ".tmp")
    temp_path.write_text(payload.content)
    temp_path.replace(path)
    return {"name": script_name, "path": str(path)}


@app.post("/api/projects/{project}/runs")
def record_run(
    project: str = FastAPIPath(...),
    payload: RunRecord = Body(...),
) -> dict:
    teleprompter_dir = _ensure_project_structure(project)
    runs_dir = teleprompter_dir / "runs"
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    safe_take = _slugify(payload.take_id)
    path = runs_dir / f"{timestamp}__{safe_take}.json"
    path.write_text(payload.model_dump_json(indent=2))
    return {"path": str(path)}


@app.post("/api/projects/{project}/scripts/{script_name}/export")
def export_script(
    project: str = FastAPIPath(...),
    script_name: str = FastAPIPath(...),
) -> dict:
    path = _script_path(project, script_name)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Script not found")

    teleprompter_dir = _ensure_project_structure(project)
    exports_dir = teleprompter_dir / "exports"

    content = path.read_text()
    stem = Path(script_name).stem

    text_export = exports_dir / f"{stem}.txt"
    prompt_export = exports_dir / f"{stem}.prompt.json"

    text_export.write_text(content)
    prompt_export.write_text(
        json.dumps(
            {
                "script": script_name,
                "project": project,
                "exported_at": datetime.utcnow().isoformat(),
                "format": Path(script_name).suffix.lstrip("."),
                "lines": content.splitlines(),
                "body": content,
            },
            indent=2,
        )
    )

    return {"exports": {"text": str(text_export), "prompt": str(prompt_export)}}


if INDEX_FILE.exists():
    app.mount("/", StaticFiles(directory=str(PUBLIC_DIR), html=True), name="static")
else:
    @app.get("/")
    def missing_ui():
        raise HTTPException(status_code=404, detail="Public index.html not found")
