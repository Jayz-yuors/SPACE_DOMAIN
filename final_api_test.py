import os
import requests

API_KEY = os.getenv("NASA_API_KEY")

if not API_KEY:
    raise RuntimeError("NASA_API_KEY not found")

url = "https://api.nasa.gov/neo/rest/v1/feed"

params = {
    "start_date": "2024-01-01",
    "end_date": "2024-01-02",
    "api_key": API_KEY
}

response = requests.get(url, params=params, timeout=10)

print("HTTP Status:", response.status_code)

data = response.json()

# Basic validation
if response.status_code == 200 and "near_earth_objects" in data:
    print("✅ API KEY IS VALID AND WORKING")
    print("Sample keys:", list(data["near_earth_objects"].keys()))
else:
    print("❌ API KEY ISSUE")
    print(data)
