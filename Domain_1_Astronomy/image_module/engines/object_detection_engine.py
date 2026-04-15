import torch
import torchvision
import torchvision.transforms as T


class ObjectDetectionEngine:
    """
    Performs object detection using pretrained Faster R-CNN.
    """

    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(
            weights="DEFAULT"
        )
        self.model.to(self.device)
        self.model.eval()

        self.transform = T.Compose([T.ToTensor()])

    def detect(self, image):
        tensor = self.transform(image).to(self.device)

        with torch.no_grad():
            predictions = self.model([tensor])[0]

        boxes = predictions["boxes"]
        scores = predictions["scores"]
        labels = predictions["labels"]

        results = []

        for i in range(len(scores)):
            if scores[i] > 0.6:
                results.append({
                    "label_id": labels[i].item(),
                    "confidence": scores[i].item(),
                    "box": boxes[i].tolist()
                })

        return results
