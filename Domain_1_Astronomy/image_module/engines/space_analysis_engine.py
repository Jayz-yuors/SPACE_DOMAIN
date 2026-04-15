import numpy as np
from Domain_1_Astronomy.image_module.ml.detection_models import StarDetectionModel


class SpaceAnalysisEngine:
    """
    Space analysis engine.
    Uses ML-ready star detection model.
    """

    def __init__(self):
        self.detector = StarDetectionModel()

    def analyze(self, image):

        star_points, cluster_labels = self.detector.detect_stars(image)

        star_count = len(star_points)

        cluster_count = 0
        if cluster_labels is not None:
            cluster_count = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)

        star_density = 0.0
        if star_count > 0:
            img_np = np.array(image)
            total_pixels = img_np.shape[0] * img_np.shape[1]
            star_density = float(star_count / total_pixels)

        return {
            "star_count": int(star_count),
            "star_density": star_density,
            "cluster_count": int(cluster_count),
            "star_points": star_points,
            "cluster_labels": cluster_labels
        }
