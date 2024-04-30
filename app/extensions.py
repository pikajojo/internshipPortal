from flask_pymongo import PyMongo
from gridfs import GridFS

mongo = PyMongo()
fs = None

def create_fs(app):
    global fs
    fs = GridFS(mongo.db)
