import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.server_api import ServerApi, ServerApiVersion
from gridfs import GridFS


#MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_URI = "mongodb+srv://bursaeacid0c:uQ0GGRYZaXAM08Pw@cluster0.l0vrjlo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#MONGODB_DB = os.getenv("MONGODB_DB")
MONGODB_DB = "apc"
# Create MongoDB client and database instance
MONGODB_CLIENT = MongoClient(MONGODB_URI)
DB = MONGODB_CLIENT[MONGODB_DB]
#DB=MONGODB_CLIENT.test
FS = GridFS(DB)