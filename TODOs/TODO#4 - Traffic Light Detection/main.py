import cv2
import numpy as np
import matplotlib.pyplot as plt

def detect_traffic_light_color(frame):
    """Detects the color of the traffic light in the frame and returns the color name."""
    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define HSV color ranges for red, yellow, and green
    red_lower1 = np.array([0, 100, 100])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([160, 100, 100])
    red_upper2 = np.array([180, 255, 255])

    yellow_lower = np.array([15, 100, 100])
    yellow_upper = np.array([35, 255, 255])

    green_lower = np.array([35, 100, 100])
    green_upper = np.array([85, 255, 255])

    # Create masks for red, yellow, and green
    red_mask1 = cv2.inRange(hsv_frame, red_lower1, red_upper1)
    red_mask2 = cv2.inRange(hsv_frame, red_lower2, red_upper2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)
    green_mask = cv2.inRange(hsv_frame, green_lower, green_upper)

    # Count the number of pixels for each color
    red_pixels = cv2.countNonZero(red_mask)
    yellow_pixels = cv2.countNonZero(yellow_mask)
    green_pixels = cv2.countNonZero(green_mask)

    # Determine which color has the most pixels
    if red_pixels > yellow_pixels and red_pixels > green_pixels:
        return "Red"
    elif yellow_pixels > red_pixels and yellow_pixels > green_pixels:
        return "Yellow"
    elif green_pixels > red_pixels and green_pixels > yellow_pixels:
        return "Green"
    else:
        return "Unknown"

def process_video_with_matplotlib(video_path):
    """Process the video frame by frame and display the frames using Matplotlib."""
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Unable to open video.")
        return

    plt.ion()  # Turn on interactive mode for real-time display

    fig, ax = plt.subplots()
    img_plot = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Exit the loop when the video ends

        # Detect the traffic light color in the current frame
        color_detected = detect_traffic_light_color(frame)

        # Overlay the detected color name on the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (0, 0, 0)  # Green text
        thickness = 2
        cv2.putText(frame, f'Color: {color_detected}', (10, 30), font, font_scale, font_color, thickness, cv2.LINE_AA)

        # Convert the frame from BGR to RGB for Matplotlib
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display the frame using Matplotlib
        if img_plot is None:
            img_plot = ax.imshow(frame_rgb)
        else:
            img_plot.set_data(frame_rgb)

        plt.draw()
        plt.pause(0.03)  # Pause to simulate video playback

    cap.release()
    plt.ioff()  # Turn off interactive mode
    plt.show()

# Test the program on a video
video_path = 'signal.mp4'  # Replace with your video path
process_video_with_matplotlib(video_path)
