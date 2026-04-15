import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import models

from Domain_1_Astronomy.image_module.ml.training.dataset_loader import SpaceImageDataset


class StarClassifier(nn.Module):
    """
    Simple CNN for star presence classification.
    """

    def __init__(self):
        super().__init__()
        self.model = models.resnet18(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features, 2)

    def forward(self, x):
        return self.model(x)


def train(image_folder, epochs=5, batch_size=8):

    dataset = SpaceImageDataset(image_folder)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = StarClassifier()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.0001)

    model.train()

    for epoch in range(epochs):
        total_loss = 0

        for images in dataloader:

            # Dummy labels (replace with real labels later)
            labels = torch.zeros(images.size(0), dtype=torch.long)

            outputs = model(images)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch [{epoch+1}/{epochs}] Loss: {total_loss:.4f}")

    torch.save(model.state_dict(), "star_classifier.pth")
    print("Star detector model saved.")