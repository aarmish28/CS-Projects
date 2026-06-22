"""
overlays.py -- this is the drawing helper functions

OVERALL THEORY EXPLAINED AGAIN:

This file contains helper functions that draw extra information on images.
The intially provided files already gave a similar overlay file, and we keep that idea.

What we use it for:
- drawing the RGB histogram as a matplotlib plot on top of the webcam frame
- drawing text lines such as filter name / stats / controls

Important idea:
Creating a matplotlib figure every frame is slow, so we create the histogram
figure once and only update the line values every frame.
"""

import numpy as np
import cv2
from matplotlib import pyplot as plt


def initialize_hist_figure():
    """
    Creating the histogram figure once.

    Here are the following Return values:
    fig, ax, background, r_plot, g_plot, b_plot

    These are reused every frame inside run.py.
    """

    # Creating a new matplotlib figure.
    fig = plt.figure()

    # Adding one axis / plot area.
    ax = fig.add_subplot(111)

    # Pixel intensities go from 0 to 255.
    ax.set_xlim([-0.5, 255.5])

    # Our histogram values are normalized into 0 to 3 range.
    ax.set_ylim([0, 3])

    # Drawing the canvas once so matplotlib prepares internal buffers.
    fig.canvas.draw()

    # Storing background for faster animation updates.
    background = fig.canvas.copy_from_bbox(ax.bbox)

    # X-axis: 0 to 255.
    x_line = np.arange(0, 256, 1)

    # Creating one animated line for each color channel.
    r_plot = ax.plot(x_line, np.zeros(256), "r", animated=True)[0]
    g_plot = ax.plot(x_line, np.zeros(256), "g", animated=True)[0]
    b_plot = ax.plot(x_line, np.zeros(256), "b", animated=True)[0]

    return fig, ax, background, r_plot, g_plot, b_plot


def update_histogram(fig, ax, background, r_plot, g_plot, b_plot, r_bars, g_bars, b_bars):
    """
    Update the histogram lines for the current frame.

    r_bars, g_bars, b_bars are arrays with 256 values each.
    """

    # Restore previous clean background.
    fig.canvas.restore_region(background)

    # Replace old y-values with new histogram values.
    r_plot.set_ydata(r_bars)
    g_plot.set_ydata(g_bars)
    b_plot.set_ydata(b_bars)

    # Redraw only the changed artists instead of the whole figure.
    ax.draw_artist(r_plot)
    ax.draw_artist(g_plot)
    ax.draw_artist(b_plot)

    # Blit = fast update of the axis region.
    fig.canvas.blit(ax.bbox)


def plot_overlay_to_image(np_img, plt_figure):
    """
    Convert a matplotlib figure into an image overlay and paste it onto np_img.

    White pixels are treated as transparent-ish background.
    """

    # Read RGBA pixel buffer from matplotlib canvas.
    rgba_buf = plt_figure.canvas.buffer_rgba()

    # Get width and height of the matplotlib canvas.
    fig_w, fig_h = plt_figure.canvas.get_width_height()

    # Convert buffer into a normal RGB image array.
    overlay_img = np.frombuffer(rgba_buf, dtype=np.uint8).reshape(fig_h, fig_w, 4)[:, :, :3]

    # Get size of target camera frame.
    img_h, img_w = np_img.shape[:2]

    # Make sure overlay does not go outside the camera frame.
    overlay_h = min(fig_h, img_h)
    overlay_w = min(fig_w, img_w)

    # Crop overlay to fit.
    overlay_crop = overlay_img[:overlay_h, :overlay_w]

    # Mask: keep only pixels that are not almost white.
    mask = np.any(overlay_crop < 250, axis=2)

    # Copy non-white overlay pixels into the camera frame.
    np_img[:overlay_h, :overlay_w][mask] = overlay_crop[mask]

    return np_img


def plot_strings_to_image(np_img, list_of_string, text_color=(255, 0, 0), right_space=430, top_space=40):
    """
    Draw a list of strings on the top-right of the image.

    This is useful for small debug/status text.
    """

    # Starting y-position for the first line.
    y_pos = top_space

    # Distance between each text line.
    line_height = 24

    # Get image size.
    h, w, _ = np_img.shape

    # x-position: near right side, but never less than 10.
    x_pos = max(10, w - right_space)

    # Draw every line one below another.
    for text in list_of_string:
        if y_pos >= h:
            break

        cv2.putText(
            np_img,
            text,
            (x_pos, y_pos),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.58,
            text_color,
            2,
            cv2.LINE_AA,
        )

        y_pos += line_height

    return np_img
