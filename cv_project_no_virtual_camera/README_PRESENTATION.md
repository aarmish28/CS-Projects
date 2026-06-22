# Computer Vision Project - Presentation Notes

## One-minute overall explanation

Our project follows a real-time Computer Vision pipeline. First, OpenCV captures live webcam frames. Then our custom processing generator applies image operations such as RGB statistics, entropy calculation, histogram equalization, linear transformation, Sobel edge detection, and the neural-network special task. Finally, the processed frames are sent through pyvirtualcam to a virtual camera that can be selected in OBS Studio.

## Main architecture

Webcam input → custom_processing() → processed frame → virtual camera output → OBS

## Files

Note: this cleaned version intentionally does not include `virtual_camera.py` or a `main.py` wrapper. The project entry point is `run.py`, and the virtual-camera logic lives directly inside `capturing.py`.


- `run.py`: main controller following professor-style generator pipeline
- `capturing.py`: webcam input and virtual camera output
- `basics.py`: mean, mode, std, min, max, entropy, RGB histogram values
- `histogram.py`: histogram equalization
- `filters.py`: Sobel edge detection
- `transformation.py`: linear brightness/contrast transform
- `special_task.py`: MediaPipe Face Mesh emoji special task
- `overlays.py`: histogram/text overlay helpers

## Keyboard controls

- T = linear transformation
- E = histogram equalization
- S = Sobel edge detection
- F = neural-network emoji special task
- Q = quit

## Important viva answers

Linear transformation: `new_pixel = alpha * old_pixel + beta`. Alpha controls contrast, beta controls brightness.

Entropy: measures how much information/detail/randomness exists in an image.

Sobel: edge detector that finds strong intensity changes.

Histogram equalization: improves contrast by spreading brightness values.

Special task: uses MediaPipe Face Mesh, a pretrained neural-network-based landmark detector, then replaces the detected face with emoji overlays.
