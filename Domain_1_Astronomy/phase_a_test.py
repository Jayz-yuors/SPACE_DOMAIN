from Domain_1_Astronomy.ingestion.api_client import NASAApiClient
from Domain_1_Astronomy.image_module.image_pipeline import ImagePipeline
import json


def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


if __name__ == "__main__":

    print_section("INITIALIZING PHASE A TEST")

    client = NASAApiClient()
    pipeline = ImagePipeline()

    apod = client.fetch_apod()

    if apod["media_type"] != "image":
        print("Today's APOD is not an image. Exiting.")
        exit()

    print_section("RUNNING FULL SCIENTIFIC ANALYSIS")

    result = pipeline.process(
        image_url=apod["url"],
        metadata=apod
    )

    # -----------------------------------------
    # Quantitative Metrics
    # -----------------------------------------
    print_section("QUANTITATIVE METRICS")
    print(json.dumps(result["quantitative_metrics"], indent=2))

    # -----------------------------------------
    # Morphological Metrics
    # -----------------------------------------
    print_section("MORPHOLOGICAL METRICS")
    print(json.dumps(result["morphological_metrics"], indent=2))

    # -----------------------------------------
    # Space Metrics
    # -----------------------------------------
    print_section("SPACE METRICS")
    print(json.dumps(result["space_metrics"], indent=2))

    # -----------------------------------------
    # Segmentation Metrics (Phase A Core)
    # -----------------------------------------
    print_section("SEGMENTATION METRICS (PHASE A)")
    print(json.dumps(result["segmentation_metrics"], indent=2))

    # -----------------------------------------
    # Gemini Output
    # -----------------------------------------
    print_section("GEMINI SCIENTIFIC INTERPRETATION")
    print(json.dumps(result["ai_interpretation"], indent=2))

    # -----------------------------------------
    # Saved Files
    # -----------------------------------------
    print_section("SAVED OUTPUT FILES")
    for path in result["saved_images"]:
        print(" -", path)

    print_section("PHASE A TEST COMPLETE")
