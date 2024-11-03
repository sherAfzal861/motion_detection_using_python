import sys
import cv2

# Get version information
python_version = f"Python version: {sys.version}"
opencv_version = f"OpenCV version: {cv2.__version__}"

# Write the version info to a text file
with open("requirements.txt", "w") as file:
    file.write(python_version + "\n")
    file.write(opencv_version + "\n")

print("Version information saved to requirements.txt")
