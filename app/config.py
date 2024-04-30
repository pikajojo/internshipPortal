from pymongo.server_api import ServerApi
import os
from pymongo import MongoClient
from gridfs import GridFS

#class Config:
    #MONGODB_URI = os.getenv("MONGODB_URI")
    #MONGODB_DB = os.getenv("MONGODB_DB")

    # Create MongoDB client and database instance
    #MONGODB_CLIENT = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
    #DB = MONGODB_CLIENT[MONGODB_DB]
    #FS = GridFS(DB)
