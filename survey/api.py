from fastapi import APIRouter
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI, OpenAIError
from gtts import gTTS
import random
from moviepy.editor import VideoFileClip
from pytube import YouTube
import imageio
import os
import uuid

class VideoProcessor:
    def __init__(self):
        self.client = OpenAI(api_key="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")

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
            return response.choices[0].message.content
        except OpenAIError as e:
            print(e)
            return None

    def generate_audio(self, text, unique_id):
        try:
            language = 'en'
            myobj = gTTS(text=text, lang=language, slow=False)
            path = f"audio/{unique_id}.mp3"
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

    def extract_random_frames(self, youtube_url, output_dir, num_frames):
        try:
            video_file = self.download_video(youtube_url, output_dir)
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

router = APIRouter()
video_processor = VideoProcessor()

@router.get("/process_video")
async def process_video():
    try:
        unique_id = uuid.uuid4()
        transcript = video_processor.get_transcript('O6-1Bd6SaXg')
        if transcript:
            summary = video_processor.generate_summary(transcript)
            if summary:
                audio_path = video_processor.generate_audio(summary, unique_id)
                video_processor.extract_random_frames('O6-1Bd6SaXg', f'frames/{unique_id}', 20)
                return {"audio_path": audio_path}
    except Exception as e:
        print(e)
        return {"error": "An error occurred during video processing."}
