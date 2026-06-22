"""
captuing.py -- professor-style input/output helper file

THE OVERALL basic theory:

This file is responsible for the boring but super important part , the main part():
--real camera / screen input to Python image stream to virtual camera output

In the base project or well, this role was handled by the VirtualCamera class.
--We keep the same idea here, because the project sheet

--expects a pipeline like: OpenCV camera to custom image processing to virtual camera

So basically:
--capture_cv_video() gives us webcam frames one-by-one
--virtual_cam_interaction() sends processed frames to OBS / Zoom / Discord

IMPORTANT NOTE:
--OpenCV normally gives BGR frames, but pyvirtualcam expects RGB frames by default.
--So in run.py we call capture_cv_video(..., bgr_to_rgb=True), and from that point
on our whole processing pipeline treats the frame as RGB.
"""

import cv2
import numpy as np
import pyvirtualcam
from PIL import ImageGrab
from matplotlib import pyplot as plt
import keyboard


class VirtualCamera:
    """
    This is a Small helper class that connects: input camera to generator frames to virtual camera output
    We use a class only to store fps / width / height once, instead of passing them manually everywhere like a confused caveman haha.
    """

    def __init__(self, fps, width, height):
        # these are the frames per second for the virtual camera output
        self.fps = fps

        # this is the width of every frame we send to the virtual camera
        self.width = width

        # this is the height of every frame we send to the virtual camera
        self.height = height

    def capture_screen(self, plt_inside=False, alt_width=0, alt_height=0):
        """
        Basically captures the primary monitor instead of the webcam.
        --This is useful if the webcam is broken or if we want to test the pipeline using the screen as input.
        It is basically, a generator, meaning it keeps yielding one image after another.
        """

        # If alternative size is given, use it. Otherwise use normal camera size.
        width = alt_width if alt_width > 0 else self.width
        height = alt_height if alt_height > 0 else self.height

        while True:
            # ImageGrab grabs a screenshot of the screen area.
            img = ImageGrab.grab(bbox=(0, 0, width, height))

            # Converting PIL image to NumPy array, because OpenCV / NumPy need arrays.
            img_np = np.array(img)

            # Optionally debug display using matplotlib.
            if plt_inside:
                plt.imshow(img_np)
                plt.axis("off")
                plt.show()

            # yield means: give this frame to whoever is consuming the generator, then continue from here next time.
            yield img_np

    def capture_cv_video(self, camera_id, bgr_to_rgb=False):
        """
        this function basically opens the real webcam using OpenCV.

        camera_id: 0 usually means default laptop webcam.

        bgr_to_rgb: OpenCV gives BGR images, but our project uses RGB for pyvirtualcam.
        --So we normally set this to True in run.py.
        """

        #Opening the real camera.
        cv_vid = cv2.VideoCapture(camera_id)

        #Here is a Safety check: if the webcam cannot open, stop immediately.
        if not cv_vid.isOpened():
            raise RuntimeError("Video input cannot be opened. Check webcam permissions / camera index.")

        # Asking the camera for our preferred width, height, codec, and FPS.
        # Cameras do not always obey perfectly, but this is the request.
        cv_vid.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cv_vid.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        cv_vid.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))
        cv_vid.set(cv2.CAP_PROP_FPS, self.fps)

        # Printing the actual camera settings so we know what we really got.
        actual_width = int(cv_vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(cv_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        actual_fps = cv_vid.get(cv2.CAP_PROP_FPS)
        print(f"Camera properties: ({actual_width}x{actual_height} @ {actual_fps}fps)")

        while True:
            # Reading one frame from webcam.
            ret, frame = cv_vid.read()

            # ret tells us if reading worked.
            if not ret:
                raise RuntimeError("Camera image cannot be loaded.")

            # Converting BGR → RGB when requested.
            # This keeps our processing and virtual camera colors correct.
            if bgr_to_rgb:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # q key stops the webcam stream.
            if keyboard.is_pressed("q"):
                cv_vid.release()
                return

            # Gives the current frame to run.py.
            yield frame

    def virtual_cam_interaction(self, img_generator, print_fps=True):
        """
        --Sends processed frames to a virtual camera.
        img_generator must be something that yields frames, for example: custom_processing(vc.capture_cv_video(...))
        --This follows the provided architecture : input generator to custom processing generator to virtual camera output
        """

        print('Quit camera stream with "q"')

        # pyvirtualcam creates a camera device that OBS / Zoom can receive.
        with pyvirtualcam.Camera(
            width=self.width,
            height=self.height,
            fps=self.fps,
            print_fps=print_fps,
        ) as cam:

            print(f"Virtual camera started: {cam.device}")

            # For every processed frame coming from run.py...
            for img in img_generator:
                # Sending the image to the virtual camera.
                cam.send(img)

                # Waiting until next frame time so the FPS stays stable.
                cam.sleep_until_next_frame()
