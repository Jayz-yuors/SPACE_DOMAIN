import os


class Config:
    """
    Central configuration for Domain_1_Astronomy
    """

    # NASA API
    NASA_API_KEY = os.environ.get("NASA_API_KEY")
    NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"
    NASA_IMAGE_SEARCH_URL = "https://images-api.nasa.gov/search"

    # Request settings
    REQUEST_TIMEOUT = 10

    # Processing configs
    MAX_VIDEO_FRAMES = 30
    IMAGE_SIZE = (224, 224)

    # Output settings
    OUTPUT_DIR = "Domain_1_Astronomy/reporting/outputs"

    @staticmethod
    def validate():
        if not Config.NASA_API_KEY:
            raise ValueError(
                "NASA_API_KEY not found in system environment variables"
            )
        else :
            print("NASA_API_KEY found and valid.")
if __name__ == "__main__":
    Config.validate()
