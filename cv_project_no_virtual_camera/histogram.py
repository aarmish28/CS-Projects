"""
histogram.py -- histogram equalization helper
OVERALL THEORY EXPLAINED:

--A histogram shows how often each pixel intensity occurs.
--For example:
    many dark pixels = histogram high near 0
    many bright pixels = histogram high near 255

The provided overlay histogram is calculated in basics.py and drawn in run.py.
This file mainly contains histogram equalization.

Histogram equalization = improves contrast by spreading brightness values more evenly.
To keep colors more natural, we equalize only the brightness channel, not each RGB
channel independently.
"""

import cv2


def equalize_histogram(frame):
    """
    Applying histogram equalization to improve contrast, because our project frame is RGB, we use YCrCb conversion from RGB.

    --Y channel: brightness / intensity
    --Cr/Cb channels: color information

    We equalize only tend to Y so colors do not become too weird.
    """

    # Converting RGB image to YCrCb color space.
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_RGB2YCrCb)

    # Spliting brightness and color channels.
    y_channel, cr_channel, cb_channel = cv2.split(ycrcb)

    # Equalizing brightness channel only.
    equalized_y = cv2.equalizeHist(y_channel)

    # Merging equalized brightness back with original color channels.
    equalized_ycrcb = cv2.merge((equalized_y, cr_channel, cb_channel))

    # Converting back to RGB for the rest of the project pipeline.
    equalized_frame = cv2.cvtColor(equalized_ycrcb, cv2.COLOR_YCrCb2RGB)

    return equalized_frame
