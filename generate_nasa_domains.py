import requests
import os

BASE_URL = "https://images-api.nasa.gov/search"

# Broad scientific seed queries
SEED_QUERIES = [
    "moon",
    "mars",
    "earth",
    "galaxy",
    "nebula",
    "solar flare",
    "asteroid",
    "saturn",
    "jupiter",
    "iss",
    "apollo",
    "hubble",
    "jwst"
]

OUTPUT_FILE = "nasa_image_domains.txt"


def fetch_metadata(query, max_pages=3):
    collected_items = []

    for page in range(1, max_pages + 1):
        params = {
            "q": query,
            "media_type": "image",
            "page": page
        }

        response = requests.get(BASE_URL, params=params, timeout=20)

        if response.status_code != 200:
            break

        data = response.json()
        items = data.get("collection", {}).get("items", [])

        if not items:
            break

        collected_items.extend(items)

    return collected_items


def extract_domains(items):
    titles = set()
    centers = set()
    keywords = set()

    for item in items:
        data_block = item.get("data", [{}])[0]

        title = data_block.get("title")
        center = data_block.get("center")
        kw = data_block.get("keywords")

        if title:
            titles.add(title.strip())

        if center:
            centers.add(center.strip())

        if kw:
            for k in kw:
                keywords.add(k.strip())

    return titles, centers, keywords


def main():
    print("Collecting NASA Image API metadata...\n")

    all_items = []

    for query in SEED_QUERIES:
        print(f"Fetching for query: {query}")
        items = fetch_metadata(query)
        all_items.extend(items)

    titles, centers, keywords = extract_domains(all_items)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("==== UNIQUE TITLES ====\n\n")
        for t in sorted(titles):
            f.write(t + "\n")

        f.write("\n\n==== UNIQUE CENTERS ====\n\n")
        for c in sorted(centers):
            f.write(c + "\n")

        f.write("\n\n==== UNIQUE KEYWORDS ====\n\n")
        for k in sorted(keywords):
            f.write(k + "\n")

    print("\nDone.")
    print(f"Saved to: {os.path.abspath(OUTPUT_FILE)}")


if __name__ == "__main__":
    main()