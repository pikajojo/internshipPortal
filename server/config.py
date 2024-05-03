import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from gridfs import GridFS

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB")

# Create MongoDB client and database instance
MONGODB_CLIENT = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
DB = MONGODB_CLIENT[MONGODB_DB]
FS = GridFS(DB)
