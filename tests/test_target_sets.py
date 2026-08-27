import os
import sys
import shutil
import pytest
from io import BytesIO
from fastapi.testclient import TestClient

# Ensure we can import uniface
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uniface.api_server import app, WORKSPACE_DIR
from uniface.core.state import state

# Disable auth for tests
state.auth = None

client = TestClient(app)

TEST_PLATFORM = "pytest_target_sets"
TEST_SET_NAME = "Test Meme Set"
SAFE_SET_NAME = "Test Meme Set"

def setup_module():
    """Clean up any previous test runs"""
    test_dir = os.path.join(WORKSPACE_DIR, TEST_PLATFORM)
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

def teardown_module():
    """Clean up after tests"""
    test_dir = os.path.join(WORKSPACE_DIR, TEST_PLATFORM)
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

def test_1_create_set():
    response = client.post(
        "/api/v1/target-sets",
        data={"name": TEST_SET_NAME},
        headers={"x-client-platform": TEST_PLATFORM}
    )
    assert response.status_code == 200
    assert response.json()["name"] == SAFE_SET_NAME

def test_2_create_duplicate_set():
    response = client.post(
        "/api/v1/target-sets",
        data={"name": TEST_SET_NAME},
        headers={"x-client-platform": TEST_PLATFORM}
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_3_upload_files():
    # Create mock files
    file1 = ("files", ("image1.jpg", b"fake_image_data_1", "image/jpeg"))
    file2 = ("files", ("image2.png", b"fake_image_data_2", "image/png"))
    
    response = client.post(
        f"/api/v1/target-sets/{SAFE_SET_NAME}/upload",
        files=[file1, file2],
        headers={"x-client-platform": TEST_PLATFORM}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["uploaded"]) == 2
    assert data["uploaded"][0]["filename"] == "image1.jpg"
    assert data["uploaded"][0]["file_id"] == f"set:{SAFE_SET_NAME}/image1.jpg"

import hashlib

def test_3b_preflight_and_link():
    # The backend now computes the real md5 hash
    real_hash_1 = hashlib.md5(b"fake_image_data_1").hexdigest()
    
    # Now check if preflight recognizes it
    response = client.post(
        "/api/v1/target-sets/preflight",
        json={"files": [{"filename": "img1.jpg", "hash": real_hash_1}, {"filename": "img3.jpg", "hash": "hash3"}]},
        headers={"x-client-platform": TEST_PLATFORM}
    )
    assert response.status_code == 200
    results = response.json()["results"]
    assert results[0]["status"] == "exists"
    assert results[1]["status"] == "new"
    
    # Try linking it to the set (as a different filename)
    link_res = client.post(
        f"/api/v1/target-sets/{SAFE_SET_NAME}/link",
        json={"files": [{"filename": "linked_img.jpg", "hash": real_hash_1}]},
        headers={"x-client-platform": TEST_PLATFORM}
    )
    assert link_res.status_code == 200
    assert len(link_res.json()["linked"]) == 1
    assert link_res.json()["linked"][0]["filename"] == "linked_img.jpg"

def test_4_list_sets():
    response = client.get(
        "/api/v1/target-sets",
        headers={"x-client-platform": TEST_PLATFORM}
    )
    assert response.status_code == 200
    sets = response.json()["target_sets"]
    assert len(sets) == 1
    assert sets[0]["name"] == SAFE_SET_NAME
    assert len(sets[0]["files"]) == 3
    filenames = [f["filename"] for f in sets[0]["files"]]
    assert "image1.jpg" in filenames
    assert "image2.png" in filenames
    assert "linked_img.jpg" in filenames

def test_5_get_media():
    response = client.get(
        f"/api/v1/target-sets/media/{SAFE_SET_NAME}/image1.jpg",
        headers={"x-client-platform": TEST_PLATFORM}
    )
    assert response.status_code == 200
    assert response.content == b"fake_image_data_1"

def test_6_delete_specific_files():
    response = client.post(
        f"/api/v1/target-sets/{SAFE_SET_NAME}/delete-files",
        json={"filenames": ["image1.jpg"]},
        headers={"x-client-platform": TEST_PLATFORM}
    )
    assert response.status_code == 200
    assert "image1.jpg" in response.json()["deleted"]
    
    # Verify it's gone
    response = client.get(
        "/api/v1/target-sets",
        headers={"x-client-platform": TEST_PLATFORM}
    )
    files = response.json()["target_sets"][0]["files"]
    assert len(files) == 1
    assert files[0]["filename"] == "image2.png"

def test_7_delete_set():
    response = client.delete(
        f"/api/v1/target-sets/{SAFE_SET_NAME}",
        headers={"x-client-platform": TEST_PLATFORM}
    )
    assert response.status_code == 200
    
    # Verify it's gone
    response = client.get(
        "/api/v1/target-sets",
        headers={"x-client-platform": TEST_PLATFORM}
    )
    assert len(response.json()["target_sets"]) == 0

if __name__ == "__main__":
    pytest.main(["-v", __file__])
