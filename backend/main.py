"""FastAPI backend for lumen-lab-147 directory file browser."""

from fastapi import FastAPI, Query, HTTPException
from pathlib import Path

app = FastAPI(
    title="lumen-lab-147 File Browser API",
    description="API for browsing directories and generating share links",
    version="0.1.0",
)


def _list_dir_recursive(dir_path: Path, max_depth: int = 3, current_depth: int = 0):
    """Recursively list directory contents up to max_depth."""
    if current_depth >= max_depth:
        return []
    
    items = []
    try:
        for item in sorted(dir_path.iterdir(), key=lambda x: (x.name, not x.is_dir())):
            entry = {
                "name": item.name,
                "path": str(item),
                "is_file": item.is_file(),
                "is_dir": item.is_dir(),
            }
            if item.is_dir():
                entry["children"] = _list_dir_recursive(item, max_depth, current_depth + 1)
            items.append(entry)
    except (PermissionError, OSError):
        pass
    return items


@app.get("/api/files", tags=["file-browser"])
def list_files(path: str = Query(..., description="Path to directory to list")):
    """List directory contents."""
    # Resolve and validate path to prevent directory traversal
    resolved = Path(path).resolve()
    base = Path(".").resolve()
    
    # Ensure resolved path is within the base directory
    try:
        resolved.relative_to(base)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Path outside allowed directory: {path}")
    
    target = resolved
    
    if not target.exists():
        raise HTTPException(status_code=404, detail=f"Path not found: {path}")
    
    if not target.is_dir():
        raise HTTPException(status_code=400, detail=f"Path is not a directory: {path}")
    
    items = _list_dir_recursive(target)
    return {"path": str(target), "items": items}


@app.get("/api/health", tags=["health"])
def health():
    """Health check endpoint."""
    return {"status": "ok", "message": "File browser API is running"}
