# from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from dotenv import load_dotenv
import os
import re

# Regex pattern
pattern = r"https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})"

load_dotenv()

# Function to fetch transcript
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine all text parts into a single string
        transcript_text = " ".join([t['text'] for t in transcript])
        return transcript_text
    except Exception as e:
        return f"Error: {e}"

# Example: Get transcript for a video
def gen_summary(url):
    match=re.match(pattern, url)
    if match is None:
        return "Invalid URL. Please provide a valid YouTube video URL."
    video_id = match.group(1)

    text = get_transcript(video_id)

    client = genai.Client(api_key=os.getenv("API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"summarize the text good readable format with bulletpoints and important keyword highlited: {text}",
    )
    return response.text

