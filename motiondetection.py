import cv2

# Set up video capture from the laptop's front camera (usually camera 0)
cap = cv2.VideoCapture(0)

# Initialize variables
first_frame = None

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    text = "No Motion"

    # Convert frame to grayscale and apply Gaussian blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Save the first frame as reference for background
    if first_frame is None:
        first_frame = gray
        continue

    # Compute absolute difference between the current frame and the first frame
    frame_delta = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

    # Dilate the threshold image to fill in holes
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours of the threshold image
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Ignore small movements
        if cv2.contourArea(contour) < 500:
            continue

        # If motion is detected, update the text and draw bounding box
        text = "Motion Detected"
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the result on the frame
    cv2.putText(frame, f"Status: {text}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("Motion Detection", frame)
    cv2.imshow("Threshold", thresh)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
