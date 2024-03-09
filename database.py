from pymongo import MongoClient

mongo_client=MongoClient('mongodb+srv://Parth:Zn5TgbeQrlO9eDdh@mycluster1.kqjgrlz.mongodb.net/?retryWrites=true&w=majority&appName=mycluster1')
db = mongo_client['youtube_videos']
collection = db['videos']