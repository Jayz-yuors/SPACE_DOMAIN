import requests

url = "https://images-api.nasa.gov/search"
params = {
    "q": "mars",
    "media_type": "image"
}

response = requests.get(url, params=params, timeout=10)
response.raise_for_status()

data = response.json()

items = data.get("collection", {}).get("items", [])
print(f"Fetched {len(items)} items")

# Inspect first item safely
if items:
    meta = items[0].get("data", [{}])[0]
    print("Title:", meta.get("title"))
    print("Date:", meta.get("date_created"))
