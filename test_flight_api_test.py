import os
import pytest
import requests
from dotenv import load_dotenv

# Load env variables
load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

# API call function for flight search
def search_flights(base_url, api_key, source, destination, date, endpoint="onewaytrip"):
    url = f"{base_url}/{endpoint}/{api_key}/{source}/{destination}/{date}"
    return requests.get(url)

# Fixtures
@pytest.fixture
def config():
    return {"base_url": BASE_URL, "api_key": API_KEY}

@pytest.fixture
def search_data():
    return [
        {"source": "DEL", "destination": "BOM", "date": "2025-07-10"},
        {"source": "BLR", "destination": "MAA", "date": "2025-07-15"},
    ]

@pytest.fixture
def invalid_data():
    return [
        {"desc": "Missing API Key", "source": "DEL", "destination": "BOM", "date": "2025-07-10", "api_key": ""},
        {"desc": "Past Date", "source": "DEL", "destination": "BOM", "date": "2022-01-01"},
    ]

# Tests
def test_search_flights(config, search_data):
    for case in search_data:
        res = search_flights(config["base_url"], config["api_key"], case["source"], case["destination"], case["date"])
        print(f"\nURL: {res.url}\nStatus: {res.status_code}\nResponse: {res.text[:300]}")
        assert res.status_code == 200
        assert res.elapsed.total_seconds() < 1.0

def test_invalid_search_cases(config, invalid_data):
    for case in invalid_data:
        key = case.get("api_key", config["api_key"])
        res = search_flights(config["base_url"], key, case["source"], case["destination"], case["date"])
        print(f"\n[Invalid Test: {case['desc']}] URL: {res.url} => Status: {res.status_code}")
        assert res.status_code in [401, 404, 410,406]
