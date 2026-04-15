import numpy as np
import cv2
from Domain_1_Astronomy.image_module.ml.segmentation_models import NebulaSegmentationModel


class SegmentationEngine:

    def __init__(self):
        self.model = NebulaSegmentationModel()

    def analyze(self, image):

        segmentation_output = self.model.segment(image)

        emission_mask = segmentation_output["emission_mask"]
        core_mask = segmentation_output["core_mask"]

        img_np = np.array(image)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # -----------------------------
        # Core Luminosity Ratio
        # -----------------------------
        core_pixels = gray[core_mask > 0]
        background_pixels = gray[core_mask == 0]

        if len(core_pixels) > 0 and len(background_pixels) > 0:
            core_mean = np.mean(core_pixels)
            background_mean = np.mean(background_pixels)
            core_luminosity_ratio = float(core_mean / (background_mean + 1e-6))
        else:
            core_luminosity_ratio = 0.0

        # -----------------------------
        # Turbulence Index (FFT)
        # -----------------------------
        f_transform = np.fft.fft2(gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude_spectrum = np.abs(f_shift)

        turbulence_index = float(np.mean(magnitude_spectrum))

        return {
            "emission_percentage": segmentation_output["emission_percentage"],
            "dark_percentage": segmentation_output["dark_percentage"],
            "core_percentage": segmentation_output["core_percentage"],
            "core_luminosity_ratio": core_luminosity_ratio,
            "turbulence_index": turbulence_index,
            "emission_mask": emission_mask,
            "dark_mask": segmentation_output["dark_mask"],
            "core_mask": core_mask
        }
