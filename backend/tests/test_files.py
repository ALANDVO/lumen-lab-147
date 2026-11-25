"""Tests for the file browser API endpoint."""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_list_files_root():
    """Test listing the root directory with path='.'"""
    response = client.get("/api/files?path=.")
    assert response.status_code == 200
    data = response.json()
    assert "path" in data
    assert "items" in data
    assert len(data["items"]) > 0


def test_list_files_with_absolute_path():
    """Test listing with absolute path within workspace."""
    response = client.get("/api/files?path=/var/lib/alan-portfolio/workspaces/alan/lumen-lab-147")
    assert response.status_code == 200
    data = response.json()
    assert data["path"] == "/var/lib/alan-portfolio/workspaces/alan/lumen-lab-147"


def test_list_files_path_traversal_blocked():
    """Test that path traversal outside workspace is blocked."""
    response = client.get("/api/files?path=/etc")
    assert response.status_code == 400
    data = response.json()
    assert "outside allowed directory" in data["detail"]


def test_list_files_not_a_directory():
    """Test that pointing to a file returns 400."""
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("test")
        tmp_path = f.name
    try:
        response = client.get(f"/api/files?path={tmp_path}")
        assert response.status_code == 400
    finally:
        os.unlink(tmp_path)


def test_list_files_include_subdirectory():
    """Test that subdirectory listing includes children."""
    response = client.get("/api/files?path=/var/lib/alan-portfolio/workspaces/alan/lumen-lab-147/backend")
    assert response.status_code == 200
    data = response.json()
    items = data["items"]
    # Find the main.py entry
    main_entry = next((item for item in items if item["name"] == "main.py"), None)
    assert main_entry is not None
    assert main_entry["is_file"] is True
    assert main_entry["is_dir"] is False

def test_list_files_health_endpoint():
    """Test the health check endpoint returns ok."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data
