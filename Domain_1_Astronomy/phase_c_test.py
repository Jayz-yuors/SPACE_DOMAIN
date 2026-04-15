from Domain_1_Astronomy.ingestion.api_client import NASAApiClient
from Domain_1_Astronomy.image_module.image_pipeline import ImagePipeline
import json


def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


if __name__ == "__main__":

    print_section("PHASE C TEST INITIALIZING")

    client = NASAApiClient()
    pipeline = ImagePipeline()

    # Fetch two different APOD entries (simulate time change)
    apod_today = client.fetch_apod()
    apod_previous = client.fetch_apod(date="2024-01-01")  # Example past date

    if apod_today["media_type"] != "image" or apod_previous["media_type"] != "image":
        print("One of the APOD entries is not an image.")
        exit()

    print_section("PROCESSING PREVIOUS IMAGE")
    result_previous = pipeline.process(
        image_url=apod_previous["url"],
        metadata=apod_previous
    )

    print_section("PROCESSING CURRENT IMAGE")
    result_current = pipeline.process(
        image_url=apod_today["url"],
        metadata=apod_today
    )

    print_section("TEMPORAL COMPARISON")
    comparison = pipeline.compare_results(
        result_previous,
        result_current
    )

    print(json.dumps(comparison, indent=2))

    print_section("PHASE C TEST COMPLETE")