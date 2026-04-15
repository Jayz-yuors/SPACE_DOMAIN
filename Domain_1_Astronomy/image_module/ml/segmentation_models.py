import numpy as np
import cv2


class NebulaSegmentationModel:
    """
    Classical segmentation model for:
    - Emission regions
    - Dark dust lanes
    - Bright core extraction
    """

    def segment(self, image):

        img_np = np.array(image)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # Enhance contrast
        gray = cv2.equalizeHist(gray)

        total_pixels = gray.size

        # -----------------------------
        # Emission Region Segmentation
        # -----------------------------
        _, emission_mask = cv2.threshold(
            gray,
            180,
            255,
            cv2.THRESH_BINARY
        )

        emission_area = np.sum(emission_mask > 0)
        emission_percentage = float(emission_area / total_pixels)

        # -----------------------------
        # Dark Dust Segmentation
        # -----------------------------
        _, dark_mask = cv2.threshold(
            gray,
            40,
            255,
            cv2.THRESH_BINARY_INV
        )

        dark_area = np.sum(dark_mask > 0)
        dark_percentage = float(dark_area / total_pixels)

        # -----------------------------
        # Bright Core Detection
        # -----------------------------
        percentile_95 = np.percentile(gray, 95)

        _, core_mask = cv2.threshold(
            gray,
            percentile_95,
            255,
            cv2.THRESH_BINARY
        )

        core_area = np.sum(core_mask > 0)
        core_percentage = float(core_area / total_pixels)

        return {
            "emission_mask": emission_mask,
            "dark_mask": dark_mask,
            "core_mask": core_mask,
            "emission_percentage": emission_percentage,
            "dark_percentage": dark_percentage,
            "core_percentage": core_percentage
        }
