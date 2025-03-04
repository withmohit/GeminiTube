from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from dotenv import load_dotenv
from pytube import YouTube
import os
import re
import isodate as iso
import asyncio
import aiohttp

# Regex pattern
pattern = r"https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})"

load_dotenv()

# Function to fetch transcript
async def get_transcript(video_id):
    try:
        transcript = await asyncio.to_thread(YouTubeTranscriptApi.get_transcript, video_id)
        transcript_text = " ".join([t['text'] for t in transcript])
        return transcript_text
    except Exception as e:
        return f"Error: {e}"

# Function to fetch video details asynchronously
async def get_video_details(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={os.getenv('GOOGLE_YOUTUBE_API_KEY')}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()

                if "items" not in data or not data["items"]:
                    return {"Error": "Video not found"}

                video = data["items"][0]
                snippet = video["snippet"]
                content_details = video["contentDetails"]

                video_details = {
                    "title": snippet["title"],
                    "channelName": snippet["channelTitle"],
                    "duration": content_details["duration"],  # ISO 8601 format
                    "thumbnail": snippet["thumbnails"]["high"]["url"]
                }
                parsed_duration = iso.parse_duration(video_details["duration"])
                video_details["duration"] = str(parsed_duration)
                
                return video_details
    except Exception as e:
        return {"Error": str(e)}

# Function to generate summary
async def gen_summary(url,collection):
    match = re.match(pattern, url)
    if match is None:
        return "Invalid URL. Please provide a valid YouTube video URL."
    
    video_id = match.group(1)
    
    #If video_id exist in db return the summary
    data = await collection.find_one({"video_id": video_id})
    if data:
        return [data["summary"],data["details"]]


    transcript, details = await asyncio.gather(
        get_transcript(video_id), 
        get_video_details(video_id)
    )
    
    client = genai.Client(api_key=os.getenv("API_KEY"))
    
    response = await asyncio.to_thread(
        client.models.generate_content,
        model="gemini-2.0-flash",
        contents=f"Summarize the given text good readable points with highlighting the crucial, scientific terms and good arguments: {transcript}"
    )
    #add into db before sending response
    await collection.insert_one({"video_id": video_id, "summary": response.text, "details": details})
    
    return [response.text, details]
