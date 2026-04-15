import os
import cv2
import json
from datetime import datetime


class AnnotationRenderer:

    def __init__(self, base_output_dir="Domain_1_Astronomy/image_outputs"):
        self.base_output_dir = base_output_dir

        if not os.path.exists(self.base_output_dir):
            os.makedirs(self.base_output_dir)

    def save_image(self, image_np, prefix="analysis"):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.jpg"
        save_path = os.path.join(self.base_output_dir, filename)

        cv2.imwrite(save_path, image_np)
        return save_path

    def save_metadata(self, metadata, prefix="analysis"):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prefix}_{timestamp}.json"
        save_path = os.path.join(self.base_output_dir, filename)

        with open(save_path, "w") as f:
            json.dump(metadata, f, indent=4)

        return save_path
