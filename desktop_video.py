import dxcam
import cv2
import numpy as np
from pynput import mouse

# Initialize global variables for the rectangle's start and end points
rect_start = None
rect_end = None

# Function to capture the first two mouse clicks
def on_click(x, y, button, pressed):
    global rect_start, rect_end
    if pressed:
        if rect_start is None:
            rect_start = (x, y)
            print(f"Start Point: {rect_start}")
        elif rect_end is None:
            rect_end = (x, y)
            print(f"End Point: {rect_end}")
            # Stop listener after second click
            return False

# Listen for mouse clicks
with mouse.Listener(on_click=on_click) as listener:
    listener.join()

# Ensure the region is within screen bounds and correct if necessary
screen_width, screen_height = 2560, 1440  # Example: Change to your screen resolution if different
rect_start = (max(0, min(screen_width, rect_start[0])), max(0, min(screen_height, rect_start[1])))
rect_end = (max(0, min(screen_width, rect_end[0])), max(0, min(screen_height, rect_end[1])))

# Calculate the region of interest (ROI) coordinates
x, y = rect_start
w, h = rect_end[0] - rect_start[0], rect_end[1] - rect_start[1]

# Ensure w and h are positive; swap if necessary
if w < 0:
    x, w = x + w, -w
if h < 0:
    y, h = y + h, -h

# Ensure the region is valid
if w == 0 or h == 0:
    print("Invalid region size. Exiting.")
    exit()

print(f"Capturing region: {x}, {y}, {w}, {h}")


# Set target FPS for capturing
target_fps = 120

# Create a desktop capture object with dxcam for the specified ROI
camera = dxcam.create(output_idx=0, output_color="BGR", region=(x, y, x+w, y+h))
camera.start(target_fps=target_fps, video_mode=True)

# Set up the video writer with the desired output file, codec, FPS, and resolution
writer = cv2.VideoWriter(
    "video.avi", cv2.VideoWriter_fourcc(*"XVID"), target_fps, (w, h)
)

if not writer.isOpened():
    print("Error: VideoWriter not initialized properly")
    camera.stop()
    exit()

# Capture frames and write to the video file
for i in range(600):
    frame = camera.get_latest_frame()
    if frame is not None:
        writer.write(frame)
    else:
        print("Error: No frame captured")
        break

# Stop capturing and release resources
camera.stop()
writer.release()
