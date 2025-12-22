# HTML Teleprompter

Modernized, single-page teleprompter with stream background, transcript library management, mirroring/split view, and customizable pacing/typography.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![DaVinci Resolve](https://img.shields.io/badge/DaVinci%20Resolve-18%2B-red.svg)

## Quick start

1. Install dependencies: `pip install -r requirements.txt`.
2. Start the dev server with hot reload: `uvicorn app.main:app --host 0.0.0.0 --port 8790 --reload`.
3. Open `http://localhost:8790` in your browser.
4. Choose a transcript from the **Transcript library** selector, upload a `.txt`/`.md` file, or type a filename from `docs/` and press **Add from docs/**.
5. Pick a **Project** to load and save scripts via the workspace API, or create one from the controls.
6. Press **Play** (or hit the space bar) to start autoscroll. Adjust speed with **+/-** or the arrow keys.
7. If `docs/list.json` cannot be fetched, the built-in `demo-list.txt` transcript will auto-load so preview links never open a blank page.

## Features

- Responsive, glassmorphism-inspired controls that stay readable over video backgrounds.
- Background options: activate the device camera or provide a network stream URL.
- Transcript sources:
  - Auto-loads `docs/list.json` alongside `index.html` (example provided for `docs/demo-list.txt`).
  - Manual fetch via "Add from docs/" for any `docs/<filename>` you place next to `index.html`.
  - Upload multiple `.txt` or `.md` files directly.
  - Persist and restore transcripts and preferences via localStorage.
  - Save and reopen scripts from workspace projects through the FastAPI service.
- Presentation tools: mirror mode, split-view clone, adjustable font size, line height, width, and speed.

## Docs list manifest

The selector boots from `docs/list.json`. Update that JSON array whenever you add or rename files inside `docs/`. Example:

```
[
  "demo-list.txt",
  "another-script.md"
]
```

If the manifest is missing, you can still type a filename into the **Add from docs/** field to fetch it manually.

When neither the manifest nor `docs/demo-list.txt` is reachable (for example, offline previews), the app injects a bundled demo script so the teleprompter always has readable content.

## Controls & shortcuts

- **Play/Pause**: button or `Space`.
- **Speed**: +/- buttons or `ArrowUp` / `ArrowDown`.
- **Toggle controls**: button or `H` / `Escape`.
- **Collapsed view**: when the toolbar is hidden, a floating Quick control keeps Play/Pause accessible.
- **Mirror / Split view**: buttons in the toolbar.

## Workspace API

- Host/port defaults: `TELEPROMPTER_HOST=0.0.0.0`, `TELEPROMPTER_PORT=8790`.
- Projects root (shared with other tools): `TELEPROMPTER_PROJECTS_ROOT=/data/projects`.
- CORS: `TELEPROMPTER_CORS_ORIGINS=*`.
- Endpoints live under `/api/projects` for listing, creating projects, managing scripts, recording runs, and exporting prompt payloads.

Run the whole stack with Docker Compose (binds port 8790 and mounts projects):

```sh
docker compose up --build
```

## Testing

Run the integrity checks and API smoke tests after installing requirements:

```sh
node tests/teleprompter.test.js
pytest
```

Launch the page in a browser to validate UX changes and streaming behavior.

---

## Stay Connected

<div align="center">
  <p>
    <a href="https://youtube.com/@Cdaprod"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube" /></a>
    <a href="https://twitter.com/cdasmktcda"><img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white" alt="Twitter" /></a>
    <a href="https://www.linkedin.com/in/cdasmkt"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
    <a href="https://github.com/Cdaprod"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>
    <a href="https://blog.min.io/author/david-cannan"><img src="https://img.shields.io/badge/Blog-FF5722?style=for-the-badge&logo=blogger&logoColor=white" alt="Blog" /></a>
  </p>
</div>

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSES.md) notice for bundled dependencies.

---

<div align="center">
  <p>
    <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FCdaprod%2FThatDAMToolbox&count_bg=%230051FF&title_bg=%23000000&icon=github.svg&icon_color=%23FFFFFF&title=Visits&edge_flat=false" alt="Repository visitors" />
  </p>
  <p><strong>Built with ❤️ by <a href="https://github.com/Cdaprod">David Cannan</a></strong><br/>Transforming how we discover, process, and manage digital media through AI.</p>
</div>

