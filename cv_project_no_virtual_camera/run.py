"""
run.py -- this is main file or well the project controller

Overall theory explained:

This file follows the professor's original code architecture:
--Real webcam input to  custom_processing() generator to virtual_cam_interaction() OBS virtual camera output

In simple words:
The webcam gives us one frame. We process that frame. Then we yield it back to the virtual camera. This happens again and again, so it becomes live video.

Keyboard controls that we have in our demo:
T = linear transformation
E = histogram equalization
S = Sobel edge detection
F = neural-network emoji special task
Q = quit

--this is the file that connects all put files hehe
"""


import time
import subprocess
import platform
import cv2
import keyboard
import numpy as np

import matplotlib
matplotlib.use("Agg")  # prevents separate matplotlib window

from capturing import VirtualCamera
from overlays import initialize_hist_figure, update_histogram
from basics import calculate_basic_stats, calculate_entropy, histogram_figure_numba
from transformation import linear_transformation
from histogram import equalize_histogram
from filters import sobel_edge_detection
from special_task import FunnyFaceEmojiTask


# ---------------------------------------------------------
# OPEN OBS AUTOMATICALLY
# ---------------------------------------------------------
def launch_obs_studio():
    """
    Open OBS automatically when the script starts.
    """
    system = platform.system()

    try:
        if system == "Darwin":  # macOS
            try:
                subprocess.Popen(["open", "-a", "OBS"])
            except Exception:
                subprocess.Popen(["open", "-a", "OBS Studio"])

        elif system == "Windows":
            subprocess.Popen([r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"])

        elif system == "Linux":
            subprocess.Popen(["obs"])

        print("Opening OBS Studio...")
        time.sleep(4)

    except Exception:
        print("Could not open OBS automatically.")
        print("Please open OBS manually.")

# Main UI colors are RGB because the project frame is RGB.
YELLOW = (0,255,255)
WHITE = (255, 255, 255)
DARK = (15, 15, 30)
PANEL_DARK = (20, 20, 35)
# ---------------------------------------------------------
# MAIN DASHBOARD
# ---------------------------------------------------------
def draw_stats_on_frame(frame, stats, entropy, mode_name):
    """
    Draw the main frontend/dashboard on the frame.
    """
    h, w, _ = frame.shape

    # ---------------- TOP BAR ----------------
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 90), (15, 15, 30), -1)
    frame = cv2.addWeighted(overlay, 0.82, frame, 0.18, 0)

    cv2.putText(
        frame,
        "Computer Vision Virtual Camera Project",
        (25, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.85,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        frame,
        f"Live OpenCV Processing + Virtual Camera Output | Mode: {mode_name}",
        (25, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        YELLOW,
        1,
        cv2.LINE_AA,
    )

    # ---------------- LEFT PANEL ----------------
    panel_x, panel_y = 20, 115
    panel_w, panel_h = 420, 260

    overlay = frame.copy()
    cv2.rectangle(
        overlay,
        (panel_x, panel_y),
        (panel_x + panel_w, panel_y + panel_h),
        (20, 20, 35),
        -1,
    )
    frame = cv2.addWeighted(overlay, 0.78, frame, 0.22, 0)

    cv2.rectangle(
        frame,
        (panel_x, panel_y),
        (panel_x + panel_w, panel_y + panel_h),
        (0, 255, 255),
        2,
    )

    cv2.putText(
        frame,
        "RGB CHANNEL STATISTICS",
        (panel_x + 15, panel_y + 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.62,
        (0, 255, 255),
        2,
        cv2.LINE_AA,
    )

    start_y = panel_y + 65

    headers = [("CH", 15), ("Mean", 60), ("Mode", 150), ("Std", 230), ("Min/Max", 300)]
    for text, x_offset in headers:
        cv2.putText(
            frame,
            text,
            (panel_x + x_offset, start_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    cv2.line(
        frame,
        (panel_x + 15, start_y + 10),
        (panel_x + panel_w - 15, start_y + 10),
        (100, 100, 100),
        1,
    )

    channel_colors = {
        "Red": (255, 80, 80),
        "Green": (80, 255, 80),
        "Blue": (80, 160, 255),
    }

    row_y = start_y + 40

    for channel_name in ["Red", "Green", "Blue"]:
        ch = stats[channel_name]
        color = channel_colors[channel_name]

        cv2.putText(frame, channel_name[0], (panel_x + 18, row_y), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
        cv2.putText(frame, f"{ch['mean']:.1f}", (panel_x + 60, row_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
        cv2.putText(frame, f"{ch['mode']}", (panel_x + 150, row_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
        cv2.putText(frame, f"{ch['std']:.1f}", (panel_x + 230, row_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
        cv2.putText(frame, f"{ch['min']}/{ch['max']}", (panel_x + 300, row_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

        row_y += 45

    # ---------------- ENTROPY ----------------
    entropy_x = panel_x + 15
    entropy_y = panel_y + 215

    cv2.rectangle(frame, (entropy_x, entropy_y), (entropy_x + 385, entropy_y + 32), (35, 35, 55), -1)

    cv2.putText(
        frame,
        f"Entropy: {entropy:.2f}",
        (entropy_x + 10, entropy_y + 22),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 255, 255),
        1,
        cv2.LINE_AA,
    )

    # ---------------- BOTTOM MENU ----------------
    menu_h = 75

    overlay = frame.copy()
    cv2.rectangle(overlay, (0, h - menu_h), (w, h), (15, 15, 30), -1)
    frame = cv2.addWeighted(overlay, 0.82, frame, 0.18, 0)

    cv2.line(frame, (0, h - menu_h), (w, h - menu_h), (0, 255, 255), 2)

    cv2.putText(
        frame,
        "MENU",
        (25, h - 43),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 255),
        2,
        cv2.LINE_AA,
    )

    controls = [
        ("T", "Linear"),
        ("E", "Equalize"),
        ("S", "Sobel"),
        ("F", "Emoji"),
        ("Q", "Quit"),
    ]

    x_pos = 110
    for key, label in controls:
        cv2.rectangle(frame, (x_pos, h - 58), (x_pos + 38, h - 25), (0, 255, 255), 2)
        cv2.putText(frame, key, (x_pos + 10, h - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, label, (x_pos + 48, h - 36), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (230, 230, 230), 1)
        x_pos += 150

    return frame


# ---------------------------------------------------------
# HISTOGRAM: SMALL + BOTTOM RIGHT
# ---------------------------------------------------------
def show_histogram_window(frame, fig):
    """
    The frame is RGB.
    The histogram image is displayed using cv2.imshow, so the line colors here
    are written in BGR order.
    """
    rgba_buf = fig.canvas.buffer_rgba()
    fig_w, fig_h = fig.canvas.get_width_height()

    hist_img = np.frombuffer(rgba_buf, dtype=np.uint8).reshape(fig_h, fig_w, 4)[:, :, :3]

    # make histogram smaller
    scale = 0.55
    hist_w = int(fig_w * scale)
    hist_h = int(fig_h * scale)
    hist_img = cv2.resize(hist_img, (hist_w, hist_h))

    frame_h, frame_w = frame.shape[:2]

    # keep it on the real bottom-right, but above the bottom menu
    margin_right = 18
    margin_bottom = 95   # keeps it above the menu bar

    x1 = frame_w - hist_w - margin_right
    y1 = frame_h - hist_h - margin_bottom
    x2 = x1 + hist_w
    y2 = y1 + hist_h

    if x1 < 0 or y1 < 0:
        return frame

    # nice dark panel behind histogram
    pad = 5
    panel_x1 = max(0, x1 - pad)
    panel_y1 = max(0, y1 - pad)
    panel_x2 = min(frame_w, x2 + pad)
    panel_y2 = min(frame_h, y2 + pad)

    overlay = frame.copy()
    cv2.rectangle(overlay, (panel_x1, panel_y1), (panel_x2, panel_y2), (18, 18, 30), -1)
    frame = cv2.addWeighted(overlay, 0.78, frame, 0.22, 0)

    cv2.rectangle(frame, (panel_x1, panel_y1), (panel_x2, panel_y2), (0, 255, 255), 1)

    # put histogram image there
    frame[y1:y2, x1:x2] = hist_img

    return frame


# ---------------------------------------------------------
# KEYBOARD DEBOUNCE
# ---------------------------------------------------------
def enough_time_passed(last_press_time, waiting_time=0.25):
    return time.time() - last_press_time > waiting_time


# ---------------------------------------------------------
# MAIN PROCESSING
# ---------------------------------------------------------
def custom_processing(img_source_generator):
    """
    Main generator:
    camera frame -> processing -> preview + OBS virtual camera
    """

    # Create histogram figure once
    fig, ax, background, r_plot, g_plot, b_plot = initialize_hist_figure()

    fig.set_size_inches(6.4, 4.8)
    fig.set_dpi(100)
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")

    ax.tick_params(colors="white", labelsize=7)
    for spine in ax.spines.values():
        spine.set_color("white")

    fig.canvas.draw()
    background = fig.canvas.copy_from_bbox(ax.bbox)

    # Create MediaPipe special task once, not every frame.
    special_task = FunnyFaceEmojiTask()

    # Mode switches. Only one main mode is active at a time.
    show_transformed = False
    show_equalized = False
    show_sobel = False
    show_special = False

    last_press_time = 0

    for frame in img_source_generator:

        # ---------------- KEYBOARD ----------------
        if enough_time_passed(last_press_time):

            if keyboard.is_pressed("t"):
                show_transformed = not show_transformed
                show_equalized = False
                show_sobel = False
                show_special = False
                last_press_time = time.time()

            elif keyboard.is_pressed("e"):
                show_equalized = not show_equalized
                show_transformed = False
                show_sobel = False
                show_special = False
                last_press_time = time.time()

            elif keyboard.is_pressed("s"):
                show_sobel = not show_sobel
                show_transformed = False
                show_equalized = False
                show_special = False
                last_press_time = time.time()

            elif keyboard.is_pressed("f"):
                show_special = not show_special
                show_transformed = False
                show_equalized = False
                show_sobel = False
                print("Emoji mode:", show_special)
                last_press_time = time.time()

        # Needed for preview window and special-task keys
        key = cv2.waitKey(1) & 0xFF
        if show_special:
            special_task.set_mode_from_key(key)

        # ---------------- APPLY MODE ----------------
        mode_name = "Original"

        if show_special:
            output_frame = special_task.process_frame(frame)
            mode_name = "Neural Emoji FaceMesh"

        elif show_sobel:
            output_frame = sobel_edge_detection(frame)
            mode_name = "Sobel Edge Detection"

        elif show_equalized:
            output_frame = equalize_histogram(frame)
            mode_name = "Histogram Equalization"

        elif show_transformed:
            output_frame = linear_transformation(frame)
            mode_name = "Linear Transformation"

        else:
            output_frame = frame.copy()

        # ---------------- CALCULATE STATS ----------------
        stats = calculate_basic_stats(output_frame)
        entropy = calculate_entropy(output_frame)

        # dashboard only in normal modes
        if not show_special:
            output_frame = draw_stats_on_frame(output_frame, stats, entropy, mode_name)

        # ---------------- UPDATE HISTOGRAM ----------------
        r_bars, g_bars, b_bars = histogram_figure_numba(output_frame)

        update_histogram(
            fig,
            ax,
            background,
            r_plot,
            g_plot,
            b_plot,
            r_bars,
            g_bars,
            b_bars,
        )

        # IMPORTANT: bottom-right placement
        output_frame = show_histogram_window(output_frame, fig)

        # ---------------- LOCAL PREVIEW WINDOW ----------------
        #preview_bgr = cv2.cvtColor(output_frame, cv2.COLOR_RGB2BGR)
        #cv2.imshow("Computer Vision Preview", preview_bgr)

        # send to OBS virtual camera
        yield output_frame


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    width = 1280
    height = 720
    fps = 20

    launch_obs_studio()

    vc = VirtualCamera(fps, width, height)

    vc.virtual_cam_interaction(
        custom_processing(
            vc.capture_cv_video(0, bgr_to_rgb=True)
        )
    )

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()