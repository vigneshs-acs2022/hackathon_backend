from fastapi import APIRouter,Request,Response,Depends
from survey.crud import Survey
from sqlalchemy.orm import Session
from .models import get_db
from youtube_transcript_api import YouTubeTranscriptApi
import openai
from gtts import gTTS 
import random
from moviepy.editor import VideoFileClip
from pytube import YouTube
import imageio
import os

survey_router = APIRouter()


@survey_router.get("/process_video")
async def get_caption_youtube():
    # retrieve the available transcripts
    transcript_list = YouTubeTranscriptApi.list_transcripts('O6-1Bd6SaXg')
    # iterate over all available transcripts
    for transcript in transcript_list:
        # translating the transcript will return another transcript object
        transcript=transcript.translate('en').fetch()

    summary = get_summary(transcript)
    audio = get_audio(summary)
    frames = extract_random_frames('O6-1Bd6SaXg', 'frames', 20)
    
    return transcript






def get_summary(instruction):
    prompt = """Provide a concise summary of the paragraph below while maintaining its original meaning and ensuring there are no grammatical errors.

    Summarize the given paragraph accurately and succinctly, preserving its meaning and adhering to proper grammar.

    Craft a brief summary of the following passage, keeping its essence intact and avoiding grammatical inaccuracies.
    """
    client = openai.OpenAI(api_key="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")
    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "user", "content": prompt},
                            {"role": "user", "content": instruction}
                        ],
                        # max_tokens=1000
                    )
    content = response.choices[0].message.content
    return content


def get_audio(text):
    # Language in which you want to convert 
    language = 'en'

    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed 
    myobj = gTTS(text=text, lang=language, slow=False) 

    # Saving the converted audio in a mp3 file named 
    # welcome 
    myobj.save("welcome.mp3")


def download_youtube_video(youtube_url, output_dir):
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(file_extension="mp4").first()
    stream.download(output_dir)
    return os.path.join(output_dir, stream.default_filename)
 
def extract_random_frames(youtube_url, output_dir, num_frames):
    video_file = download_youtube_video(youtube_url, output_dir)
    video_clip = VideoFileClip(video_file)
    duration = video_clip.duration
 
    for i in range(num_frames):
        random_time = random.uniform(0, duration)
        frame = video_clip.get_frame(random_time)
        frame_path = os.path.join(output_dir, f"frame_{i}.jpg")
        imageio.imwrite(frame_path, frame)
 
    video_clip.close()
 