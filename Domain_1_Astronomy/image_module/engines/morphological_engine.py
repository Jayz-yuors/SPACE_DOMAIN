import numpy as np
import cv2


class MorphologicalEngine:
    """
    Structural and morphological analysis for nebula/space imagery.
    Moderate complexity.
    """

    def analyze(self, image):

        img_np = np.array(image)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # Edge detection
        edges = cv2.Canny(gray, 50, 150)

        edge_density = float(np.sum(edges > 0) / edges.size)

        # Contour detection
        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        contour_count = len(contours)

        # Approximate contour complexity
        contour_complexity = float(
            np.mean([cv2.arcLength(c, True) for c in contours])
        ) if contours else 0.0

        # Symmetry estimation (horizontal flip comparison)
        flipped = cv2.flip(gray, 1)
        symmetry_score = float(
            1 - (np.mean(np.abs(gray - flipped)) / 255)
        )

        return {
            "edge_density": edge_density,
            "contour_count": contour_count,
            "average_contour_complexity": contour_complexity,
            "symmetry_score": symmetry_score
        }
