# HTML Teleprompter

Modernized, single-page teleprompter with stream background, transcript library management, mirroring/split view, and customizable pacing/typography.

## Quick start

1. Serve the repository (for example: `python -m http.server 8000`).
2. Open `http://localhost:8000` in your browser.
3. Choose a transcript from the **Transcript library** selector, upload a `.txt`/`.md` file, or type a filename from `docs/` and press **Add from docs/**.
4. Press **Play** (or hit the space bar) to start autoscroll. Adjust speed with **+/-** or the arrow keys.
5. If `docs/list.json` cannot be fetched, the built-in `demo-list.txt` transcript will auto-load so preview links never open a blank page.

## Features

- Responsive, glassmorphism-inspired controls that stay readable over video backgrounds.
- Background options: activate the device camera or provide a network stream URL.
- Transcript sources:
  - Auto-loads `docs/list.json` alongside `index.html` (example provided for `docs/demo-list.txt`).
  - Manual fetch via "Add from docs/" for any `docs/<filename>` you place next to `index.html`.
  - Upload multiple `.txt` or `.md` files directly.
  - Persist and restore transcripts and preferences via localStorage.
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
- **Mirror / Split view**: buttons in the toolbar.

## Testing

Run the lightweight integrity checks to confirm assets and defaults are present:

```sh
node tests/teleprompter.test.js
```

Launch the page in a browser to validate UX changes and streaming behavior.
