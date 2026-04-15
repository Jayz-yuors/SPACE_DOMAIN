import numpy as np
import cv2


class HeatmapEngine:
    """
    Generates intensity heatmap from image.
    """

    def generate_heatmap(self, image):
        # Convert PIL to numpy
        img_np = np.array(image)

        # Convert to grayscale
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # Normalize to 0-255
        normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

        # Apply color map
        heatmap = cv2.applyColorMap(normalized, cv2.COLORMAP_JET)

        return heatmap
