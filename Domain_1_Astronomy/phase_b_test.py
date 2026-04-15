from Domain_1_Astronomy.ingestion.api_client import NASAApiClient
from Domain_1_Astronomy.image_module.image_pipeline import ImagePipeline
import json


def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


if __name__ == "__main__":

    print_section("PHASE B TEST INITIALIZING")

    client = NASAApiClient()
    pipeline = ImagePipeline()

    apod = client.fetch_apod()

    if apod["media_type"] != "image":
        print("Today's APOD is not an image.")
        exit()

    print_section("RUNNING FULL PHASE B PIPELINE")

    result = pipeline.process(
        image_url=apod["url"],
        metadata=apod
    )

    print_section("SPACE METRICS")
    print(json.dumps(result["space_metrics"], indent=2))

    print_section("SEGMENTATION METRICS")
    print(json.dumps(result["segmentation_metrics"], indent=2))

    print_section("AI INTERPRETATION SUMMARY")
    print(result["ai_interpretation"].get("scientific_summary", "No summary"))

    print_section("SAVED OUTPUT IMAGES")
    for img in result["saved_images"]:
        print(" -", img)

    print_section("PHASE B TEST COMPLETE")