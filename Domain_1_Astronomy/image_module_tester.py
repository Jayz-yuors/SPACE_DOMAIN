from Domain_1_Astronomy.ingestion.api_client import NASAApiClient
from Domain_1_Astronomy.image_module.image_pipeline import ImagePipeline


if __name__ == "__main__":

    client = NASAApiClient()
    pipeline = ImagePipeline()

    apod = client.fetch_apod()

    if apod["media_type"] == "image":
        print("\nProcessing APOD image...\n")

        result = pipeline.process(
            image_url=apod["url"],
            metadata=apod
        )

        print("Image Type:", result["image_type"])
        print("Feature Brightness:", result["features"]["brightness"])
        print("Engine Outputs Keys:", result["engine_outputs"].keys())
