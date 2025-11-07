# Basic pytest fixtures 

import os
import sys
import json
import shutil
import importlib
from pathlib import Path
import pytest

# Make sure we can import the app
sys.path.append(os.getcwd())
import server  


def _create_sample_data(dst_dir: Path):
    """Create small fake JSON data for clubs and competitions."""
    clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
    ]
    competitions = [
        {"name": "Spring Festival", "date": "2099-03-27 10:00:00", "numberOfPlaces": "25"},
        {"name": "Fall Classic", "date": "2099-10-22 13:30:00", "numberOfPlaces": "10"},
    ]
    (dst_dir / "clubs.json").write_text(json.dumps({"clubs": clubs}), encoding="utf-8")
    (dst_dir / "competitions.json").write_text(json.dumps({"competitions": competitions}), encoding="utf-8")


@pytest.fixture(autouse=True)
def _mock_json_files(tmp_path, monkeypatch):
    """Use temp JSON files instead of real ones."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    # Copy existing or create sample data
    if Path("clubs.json").exists():
        shutil.copy("clubs.json", data_dir / "clubs.json")
        shutil.copy("competitions.json", data_dir / "competitions.json")
    else:
        _create_sample_data(data_dir)

    # Patch file paths
    monkeypatch.setattr(server, "CLUBS_PATH", str(data_dir / "clubs.json"), raising=False)
    monkeypatch.setattr(server, "COMPETITIONS_PATH", str(data_dir / "competitions.json"), raising=False)

    # Reload the app to use new paths
    importlib.reload(server)
    yield


@pytest.fixture
def client():
    """Flask test client for requests."""
    server.app.config.update(TESTING=True)
    with server.app.test_client() as c:
        yield c
