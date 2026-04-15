class ImageRouter:
    """
    Routes image to appropriate analysis engines.
    """

    def route(self, image_type: str):

        routes = {
            "diagram": ["object_detection", "diagram_analysis"],
            "earth": ["earth_analysis", "heatmap"],
            "deep_space": ["space_analysis", "heatmap"],
            "high_intensity": ["heatmap"],
            "low_light_space": ["space_analysis"],
            "general_space": ["feature_analysis"]
        }

        return routes.get(image_type, ["feature_analysis"])
