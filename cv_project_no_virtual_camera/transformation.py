"""
Transformation.py -- linear brightness/contrast transform

OVERALL THEORY EXPLAINED haha:
--Linear transformation changes every pixel using: new_pixel = alpha * old_pixel + beta

alpha: controls contrast
    --alpha > 1 = stronger contrast
    --alpha < 1 = weaker contrast

beta: controls brightness
    --beta > 0 = brighter image
    --beta < 0 = darker image

-- This satisfies the linear transformation requirement.
"""

import numpy as np


def linear_transformation(frame, alpha=1.2, beta=30):
    """
    Applying the linear transformation to an RGB frame.

    We are using NumPy directly so the formula is very obvious for presentation.
    """

    # Converting to float first, otherwise uint8 can overflow during multiplication.
    transformed = frame.astype(np.float32) * alpha + beta

    # Pixel values must stay between 0 and 255.
    transformed = np.clip(transformed, 0, 255)

    # Converting back to uint8 because images use integer pixel values.
    transformed = transformed.astype(np.uint8)

    return transformed
