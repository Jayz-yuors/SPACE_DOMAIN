import cv2


class ReportVisualizer:

    def overlay_text_block(self, image_np, text, y_offset=30):

        font = cv2.FONT_HERSHEY_SIMPLEX
        lines = text.split("\n")

        for i, line in enumerate(lines):
            cv2.putText(
                image_np,
                line,
                (20, y_offset + i * 25),
                font,
                0.6,
                (255, 255, 255),
                1,
                cv2.LINE_AA
            )

        return image_np
