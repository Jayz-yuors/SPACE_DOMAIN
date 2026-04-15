class ImageTypeClassifier:
    """
    Classifies image into broad categories.
    """
    def classify(self, metadata: dict, features: dict):

        title = (metadata.get("title") or "").lower()
        description = (metadata.get("explanation") or "").lower()

        brightness = features["brightness"]["mean_brightness"]

        # Simple keyword heuristics
        if "diagram" in title or "diagram" in description:
            return "diagram"

        if "earth" in title or "earth" in description:
            return "earth"

        if "galaxy" in title or "nebula" in title:
            return "deep_space"

        if brightness > 180:
            return "high_intensity"

        if brightness < 40:
            return "low_light_space"

        return "general_space"
