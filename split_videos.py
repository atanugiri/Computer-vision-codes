# Author: Atanu Giri
# Date: 08/30/2024

import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import cv2


# Function to select a file
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])  # Open a dialog to select a file
    return Path(file_path)


# Function to split video into four quadrants
def split_video_into_quadrants(video_path):
    # Determine the directory and create a new directory with the same name as the video file
    video_dir = video_path.parent
    video_name = video_path.stem
    video_output_dir = video_dir / video_name
    video_output_dir.mkdir(parents=True, exist_ok=True)

    # Load the video
    video = cv2.VideoCapture(str(video_path))

    # Get video dimensions
    ret, frame = video.read()
    if not ret:
        print(f"Failed to read video: {video_path}")
        return

    height, width, _ = frame.shape

    # Define the coordinates for each quadrant
    quadrants = {
        "top_left": (0, 0, width // 2, height // 2),
        "top_right": (width // 2, 0, width, height // 2),
        "bottom_left": (0, height // 2, width // 2, height),
        "bottom_right": (width // 2, height // 2, width, height),
    }

    # Iterate through each quadrant and create a separate video
    for quadrant_name, (x1, y1, x2, y2) in quadrants.items():
        quadrant_width = x2 - x1
        quadrant_height = y2 - y1

        # Create VideoWriter object
        output_filename = video_output_dir / f'{video_name}_{quadrant_name}.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_filename), fourcc, 30.0, (quadrant_width, quadrant_height))

        # Reset video capture to start from the first frame
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)

        while True:
            ret, frame = video.read()
            if not ret:
                break
            cropped_frame = frame[y1:y2, x1:x2]
            out.write(cropped_frame)

        out.release()

    video.release()
    print(f"Split videos saved to {video_output_dir}")


# Get the file from the user
video_file = select_file()
if video_file:
    # Process the selected video file
    split_video_into_quadrants(video_file)
    print("Video has been processed and saved.")
else:
    print("No file selected.")
