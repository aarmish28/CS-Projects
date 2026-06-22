"""
filters.py -- Sobel edge detection

OVERALL THEORY EXPLAINED IN GENERAL:

--The project requires at least one real filter, not an identity filter.
--We use Sobel edge detection.

Sobel basically, detects strong brightness changes.
Strong brightness changes usually mean edges / object boundaries.

Example: dark wall next to bright window to big intensity jump to edge
--Sobel X detects vertical edges.
--Sobel Y detects horizontal edges, then we combine them using magnitude.
"""

import cv2
import numpy as np


def sobel_edge_detection(frame):
    """
    Applying Sobel edge detection to an RGB frame.
    --Input: frame = RGB camera image
    --Output: RGB edge image with 3 channels, so virtual camera can send it normally.
    """

    # Converting RGB image to grayscale because edge detection is based on intensity.
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Sobel in x direction: detects left-right brightness changes.
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)

    # Sobel in y direction: detects up-down brightness changes.
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

    # Combining both directions into one edge strength image.
    sobel_combined = cv2.magnitude(sobel_x, sobel_y)

    # Normalizing edge values into visible 0..255 range.
    sobel_combined = cv2.normalize(sobel_combined, None, 0, 255, cv2.NORM_MINMAX)

    # Converting from float to uint8 image format.
    sobel_uint8 = sobel_combined.astype(np.uint8)

    # Converting grayscale edge image back to RGB 3-channel image.
    sobel_rgb = cv2.cvtColor(sobel_uint8, cv2.COLOR_GRAY2RGB)

    return sobel_rgb
