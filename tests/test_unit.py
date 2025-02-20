import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from fastapi.testclient import TestClient
from main import app  # Now this import should work
client = TestClient(app)

def test_get_company_success():
    # Assuming there's a company with ID 1 in your XML data
    response = client.get("/companies/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "MWNZ",
        "description": "..is awesome"
    }

def test_get_company_not_found():
    # Assuming there's no company with ID 9999
    response = client.get("/companies/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Failed to fetch XML"}

def test_favicon():
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/vnd.microsoft.icon"