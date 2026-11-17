# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

file-browser

## Roadmap

### file-browser — Directory file browser with share link generation

Status: planned

Acceptance:
- Backend serves directory listing via GET /api/files?path=/path
- Frontend renders file tree from API response
- Share link includes full folder context
- Tests pass for endpoint

Implementation: `backend/main.py`, `frontend/src/FileBrowser.tsx`

Tests: `backend/tests/test_files.py`

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
