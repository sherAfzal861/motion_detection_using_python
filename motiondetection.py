import cv2
import numpy as np
import time

def initialize_camera(camera_index=0):
    """Initialize video capture from the specified camera index."""
    cap = cv2.VideoCapture("cctv3.mp4")
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()
    # Give the camera some time to warm up
    time.sleep(1)
    return cap

def update_background(first_frame, gray_frame, alpha=0.05):
    """Gradually update the background to adapt to light changes."""
    return cv2.addWeighted(gray_frame, alpha, first_frame, 1 - alpha, 0)

def process_frame(frame, first_frame, min_contour_area=200):
    """Process the frame to detect motion and return the modified frame, threshold, and motion status."""
    # Convert frame to grayscale and apply Gaussian blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)  # Reduced kernel size to detect more precise changes
    
    # Calculate absolute difference between the current frame and the reference frame
    frame_delta = cv2.absdiff(first_frame, gray)
    _, thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)  # Adjusted threshold value for sensitivity
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours of the thresholded image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    motion_detected = False

    for contour in contours:
        if cv2.contourArea(contour) >= min_contour_area:
            motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Update the status text based on motion detection
    text = "Significant Motion Detected" if motion_detected else "No Motion"
    cv2.putText(frame, f"Status: {text}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    return gray, thresh, text

def main():
    # Initialize camera and variables
    cap = initialize_camera()
    first_frame = None
    min_contour_area = 2000  # Adjust this value based on your needs
    reset_interval = 100  # Frames after which to reset the background

    frame_count = 0

    while True:
        # Capture the current frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        
        # Convert frame to grayscale and set first frame as reference if not set
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if first_frame is None:
            first_frame = gray
            continue

        # Update background reference slowly to adapt to gradual lighting changes
        if frame_count % reset_interval == 0:
            first_frame = gray
        else:
            first_frame = update_background(first_frame, gray, alpha=0.01)

        # Process the frame and get the results
        _, thresh, motion_status = process_frame(frame, first_frame, min_contour_area)
        
        # Show the video feed with motion detection
        cv2.imshow("Motion Detection", frame)
        if thresh is not None:
            cv2.imshow("Threshold", thresh)

        # Increment the frame count for background reset purposes
        frame_count += 1

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
