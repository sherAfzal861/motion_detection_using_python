from moviepy.editor import VideoFileClip, vfx

# Load the video
video_path = "cctv2.mp4"  # Replace with your video file path
output_path = "cctv3.mp4"  # Define the output file name

# Load the video file
clip = VideoFileClip(video_path)

# Step 1: Cut the first 50 seconds
edited_clip = clip.subclip(50)  # Start at 50 seconds to the end

# Step 2: Increase speed (e.g., by 2x)
edited_clip = edited_clip.fx(vfx.speedx, 2)  # Change 2 to the desired speed multiplier

# Step 3: Save the final video
edited_clip.write_videofile(output_path, codec="libx264")

print("Video processing complete! Saved to", output_path)
