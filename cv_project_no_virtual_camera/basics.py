"""
basics.py -- basically the required basic image operations

OVERALL THEORY SIMPLIFIED:

in a sense a video is just many images shown very quickly.
So all functions here will work on one frame or image.
run.py (our main connector file) then calls them again and again for every webcam frame.

--so we are basically moving frame by frame

This file covers, well the following operations and statistics = 
--Mean
--Mode
--Standard deviation
--Minimum
--Maximum
--Entropy
--RGB histogram values for overlay

NOTE:
Because run.py uses capture_cv_video(..., bgr_to_rgb=True), frames here are RGB: channel 0 = Red, channel 1 = Green, channel 2 = Blue
"""

import numpy as np


def split_rgb_channels(frame):
    """
    Spliting an RGB image into Red, Green, Blue channel arrays.
    A color frame is shaped like: height × width × 3
    --The last dimension stores color channels.
    """

    # Take every row/column, channel 0 = Red.
    red = frame[:, :, 0]

    # Take every row/column, channel 1 = Green.
    green = frame[:, :, 1]

    # Take every row/column, channel 2 = Blue.
    blue = frame[:, :, 2]

    return red, green, blue


def calculate_mode(channel):
    """
    Calculating the mode of one channel.
    Mode = is basically most common pixel value.
    Since pixel values are 0..255, np.bincount is perfect here: counts[50] = how many pixels have value 50
    """

    # Flattening the 2D channel into 1D list of pixel values.
    flat = channel.flatten()

    # Counting how often every value from 0 to 255 appears.
    counts = np.bincount(flat, minlength=256)

    # Returns the index with the largest count is the most common pixel value.
    return int(np.argmax(counts))


def calculate_basic_stats(frame):
    """
    Calculating mean, mode, standard deviation, min, and max for RGB channels.
    --Return format is a dictionary so run.py can easily display it.
    """

    # Spliting the image into separate RGB channels.
    red, green, blue = split_rgb_channels(frame)

    # Storing the channels with readable names.
    channels = {
        "Red": red,
        "Green": green,
        "Blue": blue,
    }

    # here will the final results be stored , in this dictionary
    results = {}

    # Calculatign stats channel by channel.
    for name, channel in channels.items():
        results[name] = {
            # Mean = well, average brightness of this color channel.
            "mean": float(np.mean(channel)),

            # Mode = basically, most frequent pixel value.
            "mode": calculate_mode(channel),

            # Standard deviation = how spread out the values are.
            "std": float(np.std(channel)),

            # Max is brightest pixel value in this channel.
            "max": int(np.max(channel)),

            # Min is darkest pixel value in this channel.
            "min": int(np.min(channel)),
        }

    return results


def calculate_entropy(frame):
    """
    Calculating image entropy.

    Basic theory for the sake of revision:
    --Entropy measures how much information/randomness/detail is in an image.
    -Low entropy: plain wall, black image, very simple frame
    -High entropy: busy room, many textures, many edges, many intensity values

    Formula: entropy = - sum(p * log2(p))
    where p is the probability of each intensity value.
    """

    # Converting RGB frame to simple grayscale intensity using average.
    gray = np.mean(frame, axis=2).astype(np.uint8)

    # Counting how often each grayscale value occurs.
    histogram = np.bincount(gray.flatten(), minlength=256)

    # Converting the counts to probabilities.
    probabilities = histogram / np.sum(histogram)

    # Removing zero probabilities because log2(0) is, well, undefined.
    probabilities = probabilities[probabilities > 0]

    # Applying unsere entropy formula.
    entropy = -np.sum(probabilities * np.log2(probabilities))

    return float(entropy)


def histogram_figure_numba(np_img):
    """
    Calculating the normalized RGB histogram values for the provided overlay.
    The provuided overlay expects: r_bars, g_bars, b_bars
    --Each array has 256 values.
    
    We do not use numba here because pure NumPy is simple, readable, and enough
    for our project -- our code was crashing and unable to use numba , so we changed it up.
    """

    # Spliting image into RGB channels.
    red, green, blue = split_rgb_channels(np_img)

    # Counting pixel intensities for each channel.
    r_hist = np.bincount(red.flatten(), minlength=256).astype(np.float32)
    g_hist = np.bincount(green.flatten(), minlength=256).astype(np.float32)
    b_hist = np.bincount(blue.flatten(), minlength=256).astype(np.float32)

    # Avoiding division by zero just in case.
    r_max = np.max(r_hist) if np.max(r_hist) > 0 else 1
    g_max = np.max(g_hist) if np.max(g_hist) > 0 else 1
    b_max = np.max(b_hist) if np.max(b_hist) > 0 else 1

    # Normalising into 0..3 because the overlay y-axis is fixed to 0..3.
    r_bars = (r_hist / r_max) * 3.0
    g_bars = (g_hist / g_max) * 3.0
    b_bars = (b_hist / b_max) * 3.0

    return r_bars, g_bars, b_bars
