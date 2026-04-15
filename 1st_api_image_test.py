import cv2
import numpy as np
import requests
import random
from io import BytesIO
from PIL import Image
import os
from scipy.spatial import KDTree

# -------------------------------
# CONFIG
# -------------------------------
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SEARCH_URL = "https://images-api.nasa.gov/search"
QUERY = "star field"
NUM_IMAGES = 3     # multiple images for tracking
MAX_STARS = 15     # limit for clarity

# -------------------------------
# STEP 1: Fetch multiple sky images
# -------------------------------
def fetch_star_images():
    images = []

    params = {
        "q": QUERY,
        "media_type": "image",
        "page": 1
    }

    r = requests.get(SEARCH_URL, params=params, timeout=10)
    r.raise_for_status()

    items = r.json()["collection"]["items"]
    selected = random.sample(items, NUM_IMAGES)

    for idx, item in enumerate(selected):
        img_url = item["links"][0]["href"]
        img_data = requests.get(img_url, timeout=10).content
        img = Image.open(BytesIO(img_data)).convert("RGB")
        images.append(np.array(img.resize((800, 800))))

    return images

# -------------------------------
# STEP 2: Detect stars (bright spots)
# -------------------------------
def detect_stars(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    stars = []
    for cnt in contours:
        if cv2.contourArea(cnt) > 3:
            x, y, w, h = cv2.boundingRect(cnt)
            cx, cy = x + w // 2, y + h // 2
            stars.append((cx, cy))

    return stars[:MAX_STARS]

# -------------------------------
# STEP 3: Track stars across images
# -------------------------------
def track_stars(star_sets):
    tracks = {}

    base = star_sets[0]
    for i, (x, y) in enumerate(base):
        tracks[f"Star-{i+1}"] = [(x, y)]

    for stars in star_sets[1:]:
        tree = KDTree(stars)
        for name, path in tracks.items():
            last_pos = path[-1]
            _, idx = tree.query(last_pos)
            path.append(stars[idx])

    return tracks

# -------------------------------
# STEP 4: Draw paths and save output
# -------------------------------
def draw_and_save(image, tracks, index):
    output = image.copy()

    for name, points in tracks.items():
        color = tuple(np.random.randint(0, 255, 3).tolist())

        for i in range(1, len(points)):
            cv2.line(output, points[i-1], points[i], color, 2)

        x, y = points[index]
        cv2.circle(output, (x, y), 5, color, -1)
        cv2.putText(output, name, (x+5, y-5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    path = f"{OUTPUT_DIR}/star_tracking_{index+1}.png"
    cv2.imwrite(path, cv2.cvtColor(output, cv2.COLOR_RGB2BGR))
    print(f"Saved: {path}")

# -------------------------------
# MAIN PIPELINE
# -------------------------------
images = fetch_star_images()
star_sets = [detect_stars(img) for img in images]
tracks = track_stars(star_sets)

for i, img in enumerate(images):
    draw_and_save(img, tracks, i)
