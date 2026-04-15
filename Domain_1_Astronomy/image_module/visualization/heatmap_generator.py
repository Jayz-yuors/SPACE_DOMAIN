import cv2
import numpy as np


class HeatmapGenerator:

    def __init__(self, alpha=0.4):
        self.alpha = alpha

    def overlay_heatmap(self, original_image, heatmap):

        original_np = np.array(original_image)
        original_np = cv2.cvtColor(original_np, cv2.COLOR_RGB2BGR)

        heatmap_resized = cv2.resize(
            heatmap,
            (original_np.shape[1], original_np.shape[0])
        )

        combined = cv2.addWeighted(
            original_np,
            1 - self.alpha,
            heatmap_resized,
            self.alpha,
            0
        )

        return combined
