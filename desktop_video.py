import dxcam
import cv2
import numpy as np
from pynput import mouse
import threading
from datetime import datetime
import time
# Initialize global variables for the rectangle's start and end points, and a flag for stopping recording
rect_start = None
rect_end = None
stop_recording = False

# Function to capture the first two mouse clicks and stop recording on a click at (0, 0)
def on_click(x, y, button, pressed):
    global rect_start, rect_end, stop_recording
    if pressed:
        if x == 0 and y == 0:  # Check for stop condition
            print("Stop click detected. Stopping recording.")
            stop_recording = True
            return False  # Stop listener
        if rect_start is None:
            rect_start = (x, y)
            print(f"Start Point: {rect_start}")
        elif rect_end is None:
            rect_end = (x, y)
            print(f"End Point: {rect_end}")
            # Allow recording to start after second click by not stopping the listener here

# Start the listener in a non-blocking fashion
listener = mouse.Listener(on_click=on_click)
listener.start()

# Wait for the user to select the region (rect_start and rect_end to be set)
while rect_end is None:
    time.sleep(0.1)
    continue  # Busy wait; in a real application, consider a more elegant wait mechanism

# Calculate and adjust the region of interest (ROI) coordinates
x, y = rect_start
w, h = abs(rect_end[0] - rect_start[0]), abs(rect_end[1] - rect_start[1])

# Set target FPS for capturing
target_fps = 30

# Create a desktop capture object with dxcam for the specified ROI
camera = dxcam.create(output_idx=0, output_color="BGR", region=(x, y, x+w, y+h))
camera.start(target_fps=target_fps, video_mode=True)

# Generate video file name with the current date and time
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
video_file_name = f"video_{current_time}.avi"

# Set up the video writer with the desired output file, codec, FPS, and resolution
writer = cv2.VideoWriter(video_file_name, cv2.VideoWriter_fourcc(*"XVID"), target_fps, (w, h))

if not writer.isOpened():
    print("Error: VideoWriter not initialized properly")
    camera.stop()
    exit()

# Capture frames and write to the video file until stop condition is met
while not stop_recording:
    frame = camera.get_latest_frame()
    if frame is not None:
        writer.write(frame)
    else:
        print("Error: No frame captured")
        break

# Stop capturing and release resources
camera.stop()
writer.release()
listener.stop()  # Stop the mouse listener if it's still running
