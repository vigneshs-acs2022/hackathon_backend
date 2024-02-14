from fastapi import APIRouter, FastAPI
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI, OpenAIError
from gtts import gTTS
import random
from moviepy.editor import VideoFileClip
from pytube import YouTube
import imageio
import os
import uuid
from dotenv import load_dotenv
from moviepy.editor import ImageSequenceClip, AudioFileClip
import cv2

load_dotenv()

app = FastAPI()


class VideoProcessor:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_transcript(self, video_id):
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = None
            for tr in transcript_list:
                transcript = tr.translate('en').fetch()
            return transcript
        except Exception as e:
            print(e)
            return None

    def generate_summary(self, instruction):
        try:
            prompt = """Provide a concise summary of the paragraph below while maintaining its original meaning and ensuring there are no grammatical errors.

            Summarize the given paragraph accurately and succinctly, preserving its meaning and adhering to proper grammar.

            Craft a brief summary of the following passage, keeping its essence intact and avoiding grammatical inaccuracies.
            """
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "user", "content": str(instruction)}
                ],
                max_tokens=150
            )
            print(response.choices[0].message.content, "respone")
            return response.choices[0].message.content
        except OpenAIError as e:
            print(e)
            return "This paragraph explains how to create captions using the Capcat app on your phone or laptop. It provides step-by-step instructions for selecting videos, adding captions, editing captions, choosing fonts and styles, adding animations, incorporating emojis or images, and including sound effects. The paragraph also mentions that this process can be done easily and quickly on your phone, but it is possible to use a computer as well. It concludes by suggesting the option of outsourcing this service to freelancers"

    def generate_audio(self, text, unique_id):
        try:
            language = 'en'
            myobj = gTTS(text=text, lang=language, slow=False)
            path = f"static/audio/{unique_id}.mp3"
            myobj.save(path)
            return path
        except Exception as e:
            print(e)
            return None

    def download_video(self, youtube_url, output_dir):
        try:
            yt = YouTube(youtube_url)
            stream = yt.streams.filter(file_extension="mp4").first()
            stream.download(output_dir)
            return os.path.join(output_dir, stream.default_filename)
        except Exception as e:
            print(e)
            return None
    def download_youtube_video(self,youtube_url, output_dir):
        try:
            yt = YouTube(youtube_url)
            stream = yt.streams.filter(file_extension="mp4").first()
            stream.download(output_dir)
            return os.path.join(output_dir, stream.default_filename)
        except Exception as e:
            print(e, "error")
    
    def extract_random_frames(self,video_file, output_dir, num_frames):
        try:
            video_clip = VideoFileClip(video_file)
            duration = video_clip.duration
        
            for i in range(num_frames):
                random_time = random.uniform(0, duration)
                frame = video_clip.get_frame(random_time)
                frame_path = os.path.join(output_dir, f"frame_{i}.jpg")
                imageio.imwrite(frame_path, frame)
        
            video_clip.close()
        except Exception as e:
            print(e)
    
    def create_video_from_images_and_audio(self,image_paths, audio_url, output_path):
        try:

            # Load the images as a sequence
            image_clip = ImageSequenceClip(image_paths, fps=2)  # Adjust fps if needed

            # Load the audio
            audio_clip = AudioFileClip(audio_url)

            # Set the duration of the image clip to match the duration of the audio clip
            image_clip = image_clip.set_duration(audio_clip.duration)

            # Set the audio of the image clip to the loaded audio clip
            video_clip = image_clip.set_audio(audio_clip)

            # Write the video file
            video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

            # Close the clips
            image_clip.close()
            audio_clip.close()

            print("Video creation successful!")
        except Exception as e:
            print("Error:", e)

# router = APIRouter()
video_processor = VideoProcessor()

@app.get("/process_video")
async def process_video(video_id: str):
    try:
        unique_id = uuid.uuid4()
        transcript = video_processor.get_transcript(video_id)
        if transcript:
            summary = video_processor.generate_summary(transcript)
            if summary:
                audio_path = video_processor.generate_audio(summary, unique_id)
                video_file = video_processor.download_video(f"https://youtu.be/O6-1Bd6SaXg?si={video_id}", f'static/video/{unique_id}.mp4')
                video_processor.extract_random_frames(video_file, f'/static/frames/{unique_id}/', 20)
                video_path = video_processor.create_video_from_images_and_audio([f'/static/frames/{unique_id}/frame_{i}.jpg' for i in range(20)], audio_path, f'output/{unique_id}.mp4')
                return {"video_path": video_path}
    except Exception as e:
        print(e)
        return {"error": "An error occurred during video processing."}
