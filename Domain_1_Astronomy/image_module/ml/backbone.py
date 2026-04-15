import torch
import torch.nn as nn
import torchvision.models as models


class BackboneFeatureExtractor:
    """
    Shared feature extractor using pretrained ResNet.
    Removes classification head and outputs embeddings.
    """

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load pretrained ResNet18
        base_model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

        # Remove final classification layer
        self.feature_extractor = nn.Sequential(
            *list(base_model.children())[:-1]  # remove final FC layer
        )

        self.feature_extractor.to(self.device)
        self.feature_extractor.eval()

    def extract_features(self, input_tensor: torch.Tensor) -> torch.Tensor:
        """
        Returns embedding vector of image.
        """
        input_tensor = input_tensor.to(self.device)

        with torch.no_grad():
            features = self.feature_extractor(input_tensor)

        # Flatten output
        features = features.view(features.size(0), -1)

        return features

    def get_device(self):
        return self.device
