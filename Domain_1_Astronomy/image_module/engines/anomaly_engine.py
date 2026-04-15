import numpy as np
import cv2


class AnomalyEngine:

    def evaluate(self, temporal_metrics):

        score = 0

        if abs(temporal_metrics["star_count_change"]) > 500:
            score += 1

        if abs(temporal_metrics["emission_change"]) > 0.05:
            score += 1

        if abs(temporal_metrics["turbulence_change"]) > 1000:
            score += 1

        anomaly_detected = score >= 2

        return {
            "anomaly_score": score,
            "anomaly_detected": anomaly_detected
        }