import os
import random
from moviepy.editor import VideoFileClip
from pytube import YouTube
import imageio

def download_youtube_video(youtube_url, output_dir):
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(file_extension="mp4").first()
    stream.download(output_dir)
    return os.path.join(output_dir, stream.default_filename)
 
def extract_random_frames(video_file, output_dir, num_frames):
    video_clip = VideoFileClip(video_file)
    duration = video_clip.duration
 
    for i in range(num_frames):
        random_time = random.uniform(0, duration)
        frame = video_clip.get_frame(random_time)
        frame_path = os.path.join(output_dir, f"frame_{i}.jpg")
        imageio.imwrite(frame_path, frame)
 
    video_clip.close()
 
# Example usage
youtube_url = "https://www.youtube.com/watch?v=O6-1Bd6SaXg"
output_dir = "frames"
num_frames = 20
 
# Download the YouTube video and get the local file path
video_file = download_youtube_video(youtube_url, output_dir)
 
# Extract random frames from the downloaded video
extract_random_frames(video_file, output_dir, num_frames)
