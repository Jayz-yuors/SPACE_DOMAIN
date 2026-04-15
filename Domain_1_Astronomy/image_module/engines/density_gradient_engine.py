import numpy as np
import cv2


class DensityEngine:

    def compute_density_gradient(self, image):

        img_np = np.array(image)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        gradient_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gradient_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
        normalized = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)

        return normalized.astype(np.uint8)