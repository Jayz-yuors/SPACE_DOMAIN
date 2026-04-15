import requests
from PIL import Image
from io import BytesIO
import torch
import torchvision.transforms as transforms
class ImagePreprocessor:
    """
    Handles image loading and preprocessing.
    """

    def __init__(self, image_size=(224, 224)):
        self.image_size = image_size

        self.transform = transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def load_from_url(self, image_url: str) -> Image.Image:
        """
        Downloads image from URL (in memory only).
        """
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content)).convert("RGB")
        return image

    def preprocess(self, image: Image.Image) -> torch.Tensor:
        """
        Converts PIL image to normalized tensor.
        """
        tensor = self.transform(image)
        tensor = tensor.unsqueeze(0)  # Add batch dimension
        return tensor

    def process(self, image_url: str):
        """
        Full preprocessing pipeline.
        Returns:
            - original PIL image
            - preprocessed tensor
        """
        image = self.load_from_url(image_url)
        tensor = self.preprocess(image)

        return image, tensor
