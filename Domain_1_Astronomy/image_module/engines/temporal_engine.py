import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class TemporalEngine:

    def compare(self, previous_result, current_result):

        prev_features = np.array(previous_result["features"]["embedding"]).reshape(1, -1)
        curr_features = np.array(current_result["features"]["embedding"]).reshape(1, -1)

        embedding_similarity = float(cosine_similarity(prev_features, curr_features)[0][0])

        def delta(metric_name):
            return (
                current_result[metric_name]["mean_intensity"]
                - previous_result[metric_name]["mean_intensity"]
            )

        star_delta = (
            current_result["space_metrics"]["star_count"]
            - previous_result["space_metrics"]["star_count"]
        )

        emission_delta = (
            current_result["segmentation_metrics"]["emission_percentage"]
            - previous_result["segmentation_metrics"]["emission_percentage"]
        )

        turbulence_delta = (
            current_result["segmentation_metrics"]["turbulence_index"]
            - previous_result["segmentation_metrics"]["turbulence_index"]
        )

        return {
            "embedding_similarity": embedding_similarity,
            "star_count_change": star_delta,
            "emission_change": emission_delta,
            "turbulence_change": turbulence_delta
        }