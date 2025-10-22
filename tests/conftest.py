import os, sys, shutil
import pytest

# Make sure server.py can be imported
sys.path.append(os.getcwd())
import server
from server import app

@pytest.fixture(autouse=True)
def _isolate_json(tmp_path, monkeypatch):
    # Copy JSON files to a temporary folder for isolated testing
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    shutil.copy("clubs.json", data_dir / "clubs.json")
    shutil.copy("competitions.json", data_dir / "competitions.json")

    # Replace original file paths with temporary ones
    monkeypatch.setattr(server, "CLUBS_PATH", str(data_dir / "clubs.json"))
    monkeypatch.setattr(server, "COMPETITIONS_PATH", str(data_dir / "competitions.json"))
    yield

@pytest.fixture
def client():
    # Provide a test client to simulate HTTP requests
    app.config.update(TESTING=True)
    with app.test_client() as c:
        yield c
