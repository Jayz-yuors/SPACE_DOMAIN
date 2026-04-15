import os
import requests
import time

NASA_API_KEY = os.getenv("NASA_API_KEY")

if not NASA_API_KEY:
    raise RuntimeError("NASA_API_KEY not found in environment")

TIMEOUT_NORMAL = 10
TIMEOUT_SLOW = 30  # For slow APIs like Earth & Exoplanet
MAX_RETRIES = 3

def test_api(name, url, params=None, timeout=TIMEOUT_NORMAL, retries=MAX_RETRIES):
    print(f"\n🔍 Testing {name}")
    last_error = None
    
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            print("Status:", r.status_code)

            if r.status_code == 200:
                print(f"✅ {name} WORKING")
                return True
            else:
                print(f"❌ {name} FAILED (HTTP {r.status_code})")
                if r.status_code == 404:
                    print("   Endpoint not found or changed")
                elif r.status_code == 503:
                    print("   Service unavailable")
                if r.text:
                    print("   ", r.text[:150])
                last_error = f"HTTP {r.status_code}"
                
                # Retry on 503 (service unavailable)
                if r.status_code == 503 and attempt < retries:
                    print(f"   Retrying ({attempt}/{retries})...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                return False

        except requests.exceptions.Timeout:
            print(f"❌ {name} TIMEOUT (attempt {attempt}/{retries})")
            last_error = "Timeout"
            if attempt < retries:
                print(f"   Retrying with longer timeout...")
                time.sleep(2)
                continue
            return False
        except Exception as e:
            print(f"❌ {name} ERROR:", str(e)[:100])
            last_error = str(e)
            if attempt < retries:
                time.sleep(2)
                continue
            return False
    
    return False


# --------------------------------------------------
# 1️⃣ NASA Image & Video Library (NO KEY REQUIRED)
# --------------------------------------------------
test_api(
    "NASA Image & Video Library",
    "https://images-api.nasa.gov/search",
    params={"q": "space", "media_type": "image"}
)

# --------------------------------------------------
# 2️⃣ APOD (KEY REQUIRED – MAY BE DOWN)
# --------------------------------------------------
test_api(
    "APOD",
    "https://api.nasa.gov/planetary/apod",
    params={"api_key": NASA_API_KEY}
)

# --------------------------------------------------
# 3️⃣ Mars Rover Photos
# --------------------------------------------------
test_api(
    "Mars Rover Photos",
    "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/latest_photos",
    params={
        "api_key": NASA_API_KEY
    }
)

# --------------------------------------------------
# 4️⃣ EPIC
# --------------------------------------------------
test_api(
    "EPIC",
    "https://api.nasa.gov/EPIC/api/natural/images",
    params={"api_key": NASA_API_KEY}
)

# --------------------------------------------------
# 5️⃣ Earth (Landsat Metadata)
# --------------------------------------------------
test_api(
    "Earth API (Landsat)",
    "https://api.nasa.gov/planetary/earth/assets",
    params={
        "lat": 1.5,
        "lon": 100.75,
        "date": "2020-01-01",
        "api_key": NASA_API_KEY
    },
    timeout=TIMEOUT_SLOW
)

# --------------------------------------------------
# 6️⃣ DONKI (Space Weather)
# --------------------------------------------------
test_api(
    "DONKI",
    "https://api.nasa.gov/DONKI/CME",
    params={
        "startDate": "2024-01-01",
        "endDate": "2024-01-02",
        "api_key": NASA_API_KEY
    }
)

# --------------------------------------------------
# 7️⃣ NeoWs (Asteroids)
# --------------------------------------------------
test_api(
    "NeoWs",
    "https://api.nasa.gov/neo/rest/v1/feed",
    params={
        "start_date": "2024-01-01",
        "end_date": "2024-01-02",
        "api_key": NASA_API_KEY
    }
)

# --------------------------------------------------
# 8️⃣ Exoplanet Archive (NO KEY REQUIRED)
# --------------------------------------------------
test_api(
    "Exoplanet Archive",
    "https://exoplanetarchive.ipac.caltech.edu/TAP/sync",
    params={
        "query": "select top 5 pl_name from ps",
        "format": "json"
    },
    timeout=TIMEOUT_SLOW
)

print("\n🎉 NASA API FULL TEST COMPLETE")
