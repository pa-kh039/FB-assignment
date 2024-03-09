from pydantic import BaseModel
from datetime import datetime
from typing import List

class VideoBase(BaseModel):
    title: str
    description: str
    published_datetime: datetime
    thumbnail: str

class VideoCreate(VideoBase):
    pass

class Video(VideoBase):
    _id: str  # Convert ObjectId to string for serialization

    class Config:
        orm_mode = True

class PaginatedVideos(BaseModel):
    total: int
    videos: List[Video]