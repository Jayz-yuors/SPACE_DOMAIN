import requests
from Domain_1_Astronomy.config import Config


class SearchEngine:
    """
    Optimized NASA Scientific Image Search Engine.
    Filters out illustrations and non-scientific media.
    """

    def __init__(self):
        self.base_url = Config.NASA_IMAGE_SEARCH_URL

        # Words to reject
        self.reject_keywords = [
            "illustration", "artist", "concept", "rendering",
            "artwork", "cgi", "poster", "graphic",
            "animation", "digital art"
        ]

        # Scientific centers to prioritize
        self.preferred_centers = [
            "JPL", "GSFC", "STScI", "Marshall",
            "Johnson", "Langley", "Ames"
        ]

    # ----------------------------------------------------
    # SCIENTIFIC SEARCH
    # ----------------------------------------------------

    def search(self, keyword, limit=50, year_start=None, year_end=None):

        params = {
            "q": keyword,
            "media_type": "image"
        }

        if year_start:
            params["year_start"] = year_start
        if year_end:
            params["year_end"] = year_end

        response = requests.get(
            self.base_url,
            params=params,
            timeout=Config.REQUEST_TIMEOUT
        )

        response.raise_for_status()
        data = response.json()

        items = data.get("collection", {}).get("items", [])

        results = []

        for item in items:

            data_block = item.get("data", [{}])[0]
            links = item.get("links", [])

            title = (data_block.get("title") or "").lower()
            description = (data_block.get("description") or "").lower()
            center = (data_block.get("center") or "")

            # ❌ Reject illustrations
            if any(word in title for word in self.reject_keywords):
                continue
            if any(word in description for word in self.reject_keywords):
                continue

            # ✅ Prefer scientific centers
            if not any(center.startswith(pref) for pref in self.preferred_centers):
                continue

            # Validate image link
            image_url = None
            if links:
                href = links[0].get("href")
                if href and href.lower().endswith((".jpg", ".jpeg", ".png")):
                    image_url = href

            if not image_url:
                continue

            results.append({
                "title": data_block.get("title"),
                "description": data_block.get("description"),
                "date_created": data_block.get("date_created"),
                "center": center,
                "image_url": image_url
            })

            if len(results) >= limit:
                break

        return results

    # ----------------------------------------------------
    # TIME SERIES COLLECTION
    # ----------------------------------------------------

    def collect_time_series(self, keyword, year_start, year_end, limit=20):

        results = self.search(
            keyword=keyword,
            limit=limit,
            year_start=year_start,
            year_end=year_end
        )

        # Sort chronologically
        results = sorted(
            results,
            key=lambda x: x["date_created"] or ""
        )

        return results