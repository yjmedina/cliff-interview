import pytest
from fastapi.testclient import TestClient
from api.main import app, get_settings
from api.config import Settings
import pandas as pd
from pathlib import Path
import os
from api.models import LicenseUpdate

# Test settings
TEST_SETTINGS = Settings(
    input_licenses_csv="data/licenses.csv",
    output_licenses_csv="data/test_classified_licenses.csv",
    open_api_key="test-key"
)

# Override settings dependency
def override_get_settings():
    return TEST_SETTINGS

app.dependency_overrides[get_settings] = override_get_settings

client = TestClient(app)

# Test data
TEST_LICENSE = {
    "license_id": 1,
    "license_description": "Microsoft Office 365 Business",
    "category": "Productivity",
    "explanation": "Office suite for business productivity",
    "manually_validated": False
}

@pytest.fixture
def setup_test_data():
    # Create test data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Create test output file
    df = pd.DataFrame([TEST_LICENSE])
    df.to_csv(TEST_SETTINGS.output_licenses_csv, index=False)
    
    yield
    
    # Cleanup
    if os.path.exists(TEST_SETTINGS.output_licenses_csv):
        os.remove(TEST_SETTINGS.output_licenses_csv)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "License Classification API"}

def test_get_licenses_empty():
    response = client.get("/licenses")
    assert response.status_code == 200
    assert response.json() == []


def test_get_licenses_after_classification(setup_test_data):
    response = client.get("/licenses")
    assert response.status_code == 200
    licenses = response.json()
    
    assert len(licenses) == 1
    license = licenses[0]
    assert license == TEST_LICENSE 


def test_update_license(setup_test_data):
    update_data = LicenseUpdate(
        category="Productivity",
        explanation="Updated explanation"
    )
    response = client.put("/licenses/1", json=update_data.model_dump())
    assert response.status_code == 200

    license = response.json() 

    assert license["category"] == update_data.category
    assert license["explanation"] == update_data.explanation
    assert license["manually_validated"]


def test_get_summary(setup_test_data):
    response = client.get("/summary")
    assert response.status_code == 200
    summaries = response.json()
    assert len(summaries) == 1

    summary = summaries[0]

    assert summary['category'] == 'Productivity'
    assert summary['count'] == 1
    assert summary['validated_count'] == 0
    

def test_update_nonexistent_license():
    update_data = LicenseUpdate(
        category="Productivity",
        explanation="Updated explanation"
    )
    response = client.put("/licenses/999", json=update_data.model_dump())
    assert response.status_code == 404 