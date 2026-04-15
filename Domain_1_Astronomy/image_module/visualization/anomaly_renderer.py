import cv2
import numpy as np


class AnomalyRenderer:

    def render(self, image, anomaly_points):

        img_np = np.array(image)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        for point in anomaly_points:
            y, x = point
            cv2.circle(img_np, (x, y), 3, (255, 0, 255), 1)

        return img_np