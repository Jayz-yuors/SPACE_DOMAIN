import torch
import torch.nn as nn
import torch.optim as optim


class SimpleUNet(nn.Module):
    """
    Minimal U-Net style segmentation network.
    """

    def __init__(self):
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU()
        )

        self.decoder = nn.Sequential(
            nn.Conv2d(32, 16, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(16, 1, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x


def train_dummy():

    model = SimpleUNet()
    optimizer = optim.Adam(model.parameters(), lr=0.0001)
    criterion = nn.BCELoss()

    dummy_input = torch.randn(4, 3, 224, 224)
    dummy_target = torch.rand(4, 1, 224, 224)

    for epoch in range(5):
        output = model(dummy_input)
        loss = criterion(output, dummy_target)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch+1} Loss: {loss.item():.4f}")

    torch.save(model.state_dict(), "segmentation_model.pth")
    print("Segmentation model saved.")