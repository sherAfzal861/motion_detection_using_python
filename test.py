# import pyautogui
# import cv2
# import numpy as np
# import time

# # Set up video parameters
# screen_size = pyautogui.size()
# fps = 10  # Frames per second
# fourcc = cv2.VideoWriter_fourcc(*"XVID")  # Video codec

# # Create VideoWriter object
# output = cv2.VideoWriter("screen_recording.avi", fourcc, fps, screen_size)

# print("Recording... Press Ctrl+C to stop.")

# try:
#     # Start the screen recording
#     while True:
#         # Capture a screenshot using pyautogui
#         img = pyautogui.screenshot()
        
#         # Convert the screenshot to a numpy array
#         frame = np.array(img)
        
#         # Convert it from RGB (pyautogui format) to BGR (OpenCV format)
#         frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
#         # Write the frame to the video file
#         output.write(frame)
        
#         # Set a delay to match the FPS
#         time.sleep(1 / fps)

# except KeyboardInterrupt:
#     # Stop recording when user interrupts with Ctrl+C
#     print("\nRecording stopped.")

# finally:
#     # Release the video writer object
#     output.release()
#     print("Video saved as 'screen_recording.avi'")



import cv2

# Initialize the camera (0 is usually the default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture each frame
    ret, frame = cap.read()

    # Check if frame was captured successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, 6)
    gray_frame = cv2.GaussianBlur(gray_frame, (25, 25), 0)
    # Display the grayscale frame
    cv2.imshow("Grayscale Camera Feed", gray_frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
