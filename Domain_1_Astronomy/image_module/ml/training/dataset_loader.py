import os
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as transforms


class SpaceImageDataset(Dataset):
    """
    Basic dataset loader for space images.
    For now: classification or unsupervised feature training.
    """

    def __init__(self, image_folder, transform=None):
        self.image_folder = image_folder
        self.image_files = [
            f for f in os.listdir(image_folder)
            if f.lower().endswith((".jpg", ".png", ".jpeg"))
        ]

        self.transform = transform or transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = os.path.join(self.image_folder, self.image_files[idx])
        image = Image.open(img_path).convert("RGB")

        if self.transform:
            image = self.transform(image)

        return image