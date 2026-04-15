from Domain_1_Astronomy.ingestion.api_client import NASAApiClient
from Domain_1_Astronomy.image_module.image_pipeline import ImagePipeline
import json


if __name__ == "__main__":

    client = NASAApiClient()
    pipeline = ImagePipeline()

    apod = client.fetch_apod()

    if apod["media_type"] == "image":

        print("\nRunning Full Scientific Image Analysis...\n")

        result = pipeline.process(
            image_url=apod["url"],
            metadata=apod
        )

        print("\n--- Quantitative Metrics ---")
        print(json.dumps(result["quantitative_metrics"], indent=2))

        print("\n--- Morphological Metrics ---")
        print(json.dumps(result["morphological_metrics"], indent=2))

        print("\n--- Space Metrics ---")
        print(json.dumps(result["space_metrics"], indent=2))

        print("\n--- Gemini Scientific Interpretation ---")
        print(json.dumps(result["ai_interpretation"], indent=2))

        print("\nSaved Images:")
        for path in result["saved_images"]:
            print(" -", path)
