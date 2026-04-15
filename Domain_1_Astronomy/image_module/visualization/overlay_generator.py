import cv2
import numpy as np


class OverlayGenerator:

    def __init__(self, box_color=(0, 255, 0), thickness=2):
        self.box_color = box_color
        self.thickness = thickness

    def draw_boxes(self, image, detections):

        img_np = np.array(image)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        for idx, det in enumerate(detections):

            x1, y1, x2, y2 = map(int, det["box"])
            confidence = det["confidence"]

            cv2.rectangle(
                img_np,
                (x1, y1),
                (x2, y2),
                self.box_color,
                self.thickness
            )

            label_text = f"Region {idx+1} ({confidence:.2f})"

            cv2.putText(
                img_np,
                label_text,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                self.box_color,
                1
            )

        return img_np

    def draw_segmentation(self, image, emission_mask, dark_mask, core_mask):

        img_np = np.array(image)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        overlay = img_np.copy()

        # Emission regions (Green)
        overlay[emission_mask > 0] = [0, 255, 0]

        # Dark dust regions (Blue)
        overlay[dark_mask > 0] = [255, 0, 0]

        # Core regions (Red)
        overlay[core_mask > 0] = [0, 0, 255]

        blended = cv2.addWeighted(img_np, 0.7, overlay, 0.3, 0)

        return blended
