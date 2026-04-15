import numpy as np
from PIL import Image
import torch
class FeatureEngine:
    """
    Extracts measurable image features.
    """

    def __init__(self, backbone_extractor):
        self.backbone = backbone_extractor

    def extract_embedding(self, tensor: torch.Tensor):
        features = self.backbone.extract_features(tensor)
        return features.squeeze().cpu().numpy()

    def brightness_stats(self, image: Image.Image):
        gray = image.convert("L")
        arr = np.array(gray)

        return {
            "mean_brightness": float(np.mean(arr)),
            "std_brightness": float(np.std(arr)),
            "min_brightness": int(np.min(arr)),
            "max_brightness": int(np.max(arr))
        }

    def rgb_histogram(self, image: Image.Image):
        arr = np.array(image)

        histogram = {
            "red_mean": float(np.mean(arr[:, :, 0])),
            "green_mean": float(np.mean(arr[:, :, 1])),
            "blue_mean": float(np.mean(arr[:, :, 2]))
        }

        return histogram

    def extract_all_features(self, image, tensor):
        return {
            "embedding": self.extract_embedding(tensor).tolist(),
            "brightness": self.brightness_stats(image),
            "color_distribution": self.rgb_histogram(image)
        }
