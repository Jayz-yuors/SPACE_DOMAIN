import cv2
import numpy as np


class DensityRenderer:

    def render(self, image, density_map):

        img_np = np.array(image)
        img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        colored_density = cv2.applyColorMap(density_map, cv2.COLORMAP_JET)

        blended = cv2.addWeighted(img_np, 0.6, colored_density, 0.4, 0)

        return blended