import numpy as np
import cv2
from skimage.measure import shannon_entropy


class QuantitativeEngine:
    """
    Computes measurable scientific metrics from space images.
    Moderate complexity. Physically meaningful.
    """

    def analyze(self, image):
        """
        image: PIL Image
        returns: dictionary of quantitative metrics
        """

        # Convert to grayscale
        img_np = np.array(image)
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)

        # Basic brightness statistics
        mean_intensity = float(np.mean(gray))
        variance_intensity = float(np.var(gray))
        std_intensity = float(np.std(gray))

        # Histogram analysis
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist = hist.flatten()

        peak_intensity = int(np.argmax(hist))

        # Contrast (Michelson approximation)
        min_intensity = float(np.min(gray))
        max_intensity = float(np.max(gray))

        if (max_intensity + min_intensity) != 0:
            contrast_index = float(
                (max_intensity - min_intensity) /
                (max_intensity + min_intensity)
            )
        else:
            contrast_index = 0.0

        # Entropy (information richness)
        entropy_value = float(shannon_entropy(gray))

        # Signal-to-noise approximation
        if std_intensity != 0:
            snr = float(mean_intensity / std_intensity)
        else:
            snr = 0.0

        return {
            "mean_intensity": mean_intensity,
            "variance_intensity": variance_intensity,
            "std_intensity": std_intensity,
            "histogram_peak_intensity": peak_intensity,
            "contrast_index": contrast_index,
            "entropy": entropy_value,
            "signal_to_noise_ratio": snr
        }
