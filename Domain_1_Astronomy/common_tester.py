import torch
import numpy as np
from PIL import Image

from Domain_1_Astronomy.image_module.engines.feature_engine import FeatureEngine
from Domain_1_Astronomy.image_module.classifiers.image_type_classifier import ImageTypeClassifier

class DummyBackbone:
    def extract_features(self, tensor):
        # Simulate feature extraction: return a fixed-size tensor
        return torch.ones((1, 128))

def main():
    # Create a dummy image (RGB, 64x64)
    image = Image.fromarray(np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8))
    tensor = torch.rand((1, 3, 64, 64))

    # Initialize FeatureEngine with dummy backbone
    backbone = DummyBackbone()
    feature_engine = FeatureEngine(backbone)

    # Extract features
    embedding = feature_engine.extract_embedding(tensor)
    brightness = feature_engine.brightness_stats(image)
    color_dist = feature_engine.rgb_histogram(image)
    all_features = feature_engine.extract_all_features(image, tensor)

    print("Embedding shape:", embedding.shape)
    print("Brightness stats:", brightness)
    print("Color distribution:", color_dist)
    print("All features:", all_features)

    # Test ImageTypeClassifier
    classifier = ImageTypeClassifier()
    metadata = {"title": "Galaxy Image", "explanation": "A beautiful galaxy."}
    label = classifier.classify(metadata, all_features)
    print("Predicted label:", label)

if __name__ == "__main__":
    main()
"""
Common Tester for feature_engine - image_classifier - router"""