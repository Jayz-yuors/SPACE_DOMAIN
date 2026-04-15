import numpy as np
import cv2
from sklearn.cluster import DBSCAN


class StarDetectionModel:
    """
    ML-ready star detection module.
    Currently classical CV-based.
    Can be replaced later with CNN detector.
    """

    def detect_stars(self, image):

        img_np = np.array(image)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        gray = cv2.equalizeHist(gray)

        # Adaptive threshold
        thresh = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            -2
        )

        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)

        star_points = []

        for i in range(1, num_labels):

            area = stats[i, cv2.CC_STAT_AREA]

            if 4 <= area <= 40:
                star_points.append(centroids[i])

        star_points = np.array(star_points)

        # Cluster stars
        cluster_labels = None
        if len(star_points) > 10:
            clustering = DBSCAN(eps=20, min_samples=5).fit(star_points)
            cluster_labels = clustering.labels_

        return star_points, cluster_labels
