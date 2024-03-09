from fastapi import status, HTTPException, APIRouter, Query
from typing import List

from database import collection
from models import PaginatedVideos

router=APIRouter(prefix="",tags=['youtube'])

# Define API endpoint to retrieve paginated videos
@router.get('/videos/', status_code=status.HTTP_200_OK, response_model=PaginatedVideos)
def get_videos(page: int = Query(1, ge=1), per_page: int = Query(10, ge=1)):
    # Fetch videos from MongoDB sorted by published datetime in descending order
    try:
        videos = collection.find().sort('published_datetime', -1).skip((page - 1) * per_page).limit(per_page)
        result=[ {**video, '_id': str(video['_id'])} for video in videos]
        return PaginatedVideos(total=len(result), videos=result)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))