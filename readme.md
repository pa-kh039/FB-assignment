# Project Goal

To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

# Features:

- Server calls the YouTube API continuously in background (async) with some interval (say 10 seconds) for fetching the latest videos for a predefined search query and should store the data of vid eos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes.
- A GET API returns the stored video data in a paginated response sorted in descending order of published datetime.
- Scalable and optimised.
- Support for multiple API keys so that if quota is exhausted on one, it automatically uses the next available key.
- Tech Stack: FastAPI, MongoDB

# Steps to run

1. `git clone https://github.com/pa-kh039/FB-assignment.git` - to clone the repository
2. `pip install -r requirements.txt` - to install packages
3. create a .env file in the same location as 'main.py'
file. [you can create as many api keys you want for testing and put them in .env file]
sample file format of .env file:
```
total_api_keys=5

youtube_data_apikey1 = 'xxx'
youtube_data_apikey2 = 'yyy'
youtube_data_apikey3 = 'zzz'
youtube_data_apikey4 = 'aaa'
youtube_data_apikey5 = 'bbb'
```
4. You can enable youtube data api v3 and generate API keys from https://console.cloud.google.com/
5. `uvicorn main:app --reload` - run inside project directory to run server
6. open browser and use `http://127.0.0.1:8000/videos/?page=1&per_page=10` to test the API. Modify page and per_page(page size) parameters as per your need.