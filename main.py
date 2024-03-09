# main.py
import os
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, Query
from apscheduler.schedulers.background import BackgroundScheduler
from googleapiclient.discovery import build
import googleapiclient.errors
from dotenv import load_dotenv

from database import collection
from routers import youtube

load_dotenv()

app = FastAPI()

app.include_router(youtube.router)

# Replace with your YouTube API key(s)
total_api_keys = int(os.getenv("total_api_keys"))
API_KEYS = []
for i in range(1,total_api_keys+1):
    API_KEYS.append(os.getenv(f"youtube_data_apikey{i}"))
# print(API_KEYS)
API_KEY_INDEX = 0

# YouTube API setup
youtube = build('youtube', 'v3', developerKey=API_KEYS[API_KEY_INDEX])

# Fetch and store videos in the background using APScheduler
scheduler = BackgroundScheduler()

date_string = "01/03/2024"
date_format = "%m/%d/%Y"
desired_date = datetime.strptime(date_string, date_format)
rfc3339_timestamp = desired_date.replace(tzinfo=timezone.utc).isoformat()

def fetch_and_store_videos():
    global API_KEY_INDEX
    try:
        search_query = "Gaming Highlights and Let's Plays"  # Replace with your desired search query
        request = youtube.search().list(q=search_query, part='snippet', type='video', order='date',publishedAfter=rfc3339_timestamp, maxResults=10)
        response = request.execute()

        videos = []
        for item in response['items']:
            video_data = {
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'published_datetime': item['snippet']['publishedAt'],
                'thumbnail': item['snippet']['thumbnails']['default']['url'],
            }
            videos.append(video_data)

        # Store videos in MongoDB
        collection.insert_many(videos)
        print(f'{len(videos)} videos successfully stored in the database.')
    # except Exception as e:
    #     print(e)
    except googleapiclient.errors.HttpError:
        # Switch to the next API key if the current one's quota is exhausted
        print("switching API key..")
        API_KEY_INDEX = (API_KEY_INDEX + 1) % total_api_keys
        youtube.developerKey = API_KEYS[API_KEY_INDEX]

# Schedule the video fetching job every 10 seconds
scheduler.add_job(fetch_and_store_videos, 'interval', seconds=10)
scheduler.start()


