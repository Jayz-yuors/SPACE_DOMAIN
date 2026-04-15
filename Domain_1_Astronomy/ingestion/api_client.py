import requests
from Domain_1_Astronomy.config import Config


class NASAApiClient:

    def __init__(self):
        Config.validate()
        self.api_key = Config.NASA_API_KEY

    
    def fetch_apod(self, date=None):
        """Fetch APOD.If date is provided, fetch that date.Format: YYYY-MM-DD
        """
        params = {
            "api_key": self.api_key
        }

        if date:
            params["date"] = date

        response = requests.get(
            Config.NASA_APOD_URL,   # <-- USE CONFIG
            params=params,
            timeout=Config.REQUEST_TIMEOUT
        )

        response.raise_for_status()

        return response.json()
    def search_images(self, query="galaxy", limit=5):
        """
        Search NASA Image Library
        """
        params = {
            "q": query,
            "media_type": "image"
        }

        response = requests.get(
            Config.NASA_IMAGE_SEARCH_URL,
            params=params,
            timeout=Config.REQUEST_TIMEOUT
        )

        response.raise_for_status()
        data = response.json()

        items = data.get("collection", {}).get("items", [])[:limit]

        results = []

        for item in items:
            data_block = item.get("data", [{}])[0]
            links = item.get("links", [])

            image_url = None
            if links:
                image_url = links[0].get("href")

            results.append({
                "title": data_block.get("title"),
                "description": data_block.get("description"),
                "image_url": image_url
            })

        return results
if __name__ == "__main__":
    print("Initializing NASA API Client...")
    
    client = NASAApiClient()

    print("\nFetching APOD...")
    apod = client.fetch_apod()
    print(apod)

    print("\nSearching images for 'nebula'...")
    results = client.search_images("nebula")
    print(results)

