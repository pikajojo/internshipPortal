import ssl

from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://w5jingyi:MwHwgC2FbtpW95Kr@cluster0.geio7un.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(
    uri,
    tls=True,  # Changed from ssl to tls
    tlsAllowInvalidCertificates=True
)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

## import database
db = client.users
collection = db.db1
for document in collection.find():
    print(document)


def insert_document(document):
    collection.insert_one(document)


def find_document(query):
    return collection.find_one(query)


def find_all_documents():
    return list(collection.find({}))


def update_document(query, new_values):
    collection.update_one(query, {"$set": new_values})


def delete_document(query):
    collection.delete_one(query)
