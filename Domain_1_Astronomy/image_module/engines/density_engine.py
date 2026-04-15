import numpy as np
import cv2


class DensityEngine:
    """
    Computes spatial star density gradient map.
    """

    def compute_density_map(self, image, star_points, kernel_size=25):

        img_np = np.array(image)
        h, w = img_np.shape[:2]

        density_map = np.zeros((h, w), dtype=np.float32)

        for point in star_points:
            x, y = int(point[0]), int(point[1])
            if 0 <= x < w and 0 <= y < h:
                density_map[y, x] += 1

        density_map = cv2.GaussianBlur(density_map, (kernel_size, kernel_size), 0)

        # Normalize
        density_map = cv2.normalize(density_map, None, 0, 255, cv2.NORM_MINMAX)

        return density_map.astype(np.uint8)