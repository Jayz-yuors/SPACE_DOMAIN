import requests
from Domain_1_Astronomy.config import Config


class QueryReliabilityChecker:
    """
    Checks whether a grammatically corrected query
    actually returns scientific image data from NASA API.
    """

    def __init__(self):
        self.base_url = Config.NASA_IMAGE_SEARCH_URL

        self.reject_keywords = [
            "illustration", "artist", "concept",
            "rendering", "artwork", "cgi",
            "poster", "graphic", "animation",
            "digital art"
        ]

    # ----------------------------------------------------
    # VALIDATE QUERY AGAINST NASA IMAGE API
    # ----------------------------------------------------

    def validate(self, query, max_suggestions=50):

        params = {
            "q": query,
            "media_type": "image"
        }

        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=Config.REQUEST_TIMEOUT
            )

            response.raise_for_status()
            data = response.json()

        except Exception as e:
            return {
                "is_valid": False,
                "error": str(e),
                "result_count": 0,
                "suggestions": []
            }

        items = data.get("collection", {}).get("items", [])

        valid_results = []

        for item in items:

            data_block = item.get("data", [{}])[0]
            links = item.get("links", [])

            title = (data_block.get("title") or "").lower()
            description = (data_block.get("description") or "").lower()

            # ❌ Reject non-scientific content
            if any(word in title for word in self.reject_keywords):
                continue
            if any(word in description for word in self.reject_keywords):
                continue

            image_url = None
            if links:
                href = links[0].get("href")
                if href and href.lower().endswith((".jpg", ".jpeg", ".png")):
                    image_url = href

            if not image_url:
                continue

            valid_results.append({
                "title": data_block.get("title"),
                "date_created": data_block.get("date_created"),
                "center": data_block.get("center"),
                "image_url": image_url
            })

            if len(valid_results) >= max_suggestions:
                break

        return {
            "is_valid": len(valid_results) > 0,
            "result_count": len(valid_results),
            "suggestions": valid_results
        }