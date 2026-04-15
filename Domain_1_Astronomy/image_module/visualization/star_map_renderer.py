import cv2
import numpy as np


class StarMapRenderer:

    def render(self, image, star_points, cluster_labels=None):

        img_np = np.array(image)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Draw star points
        for point in star_points:
            x, y = int(point[0]), int(point[1])
            cv2.circle(img_np, (x, y), 2, (0, 255, 255), -1)

        # Draw cluster boundaries
        if cluster_labels is not None:

            unique_clusters = set(cluster_labels)

            for cluster_id in unique_clusters:

                if cluster_id == -1:
                    continue

                cluster_points = star_points[cluster_labels == cluster_id]

                if len(cluster_points) < 3:
                    continue

                hull = cv2.convexHull(cluster_points.astype(np.float32))
                hull = hull.astype(int)

                cv2.polylines(
                    img_np,
                    [hull],
                    isClosed=True,
                    color=(0, 0, 255),
                    thickness=2
                )

                # Label cluster
                centroid = np.mean(cluster_points, axis=0)
                cx, cy = int(centroid[0]), int(centroid[1])

                cv2.putText(
                    img_np,
                    f"Cluster {cluster_id}",
                    (cx, cy),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    1
                )

        return img_np
