import sys
import os

# Add the src directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
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


# Malformed XML string
malformed_xml = "<Data><id>1<id><name>Company Name</name><description>Description</description>"

def test_malformed_xml():
    # Mock the httpx.AsyncClient.get method to return a response with malformed XML
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = malformed_xml

        response = client.get("/companies/1")

        assert response.status_code == 500
        assert "Error processing XML" in response.json()["detail"]


def generate_xml_with_root(root_name):
    return f"""
<{root_name}>
    <id>1</id>
    <name>Company A</name>
    <description>A description</description>
</{root_name}>
"""

def test_configurable_root_element():
    # Generate XML with a configurable root element name
    root_name = "CustomRoot"
    xml_data = generate_xml_with_root(root_name)

    # Mock the httpx.AsyncClient.get method to return the generated XML
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = xml_data

        response = client.get("/companies/1")

        # Assertions
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "Company A",
            "description": "A description"
        }
