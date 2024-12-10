from pymongo.mongo_client import MongoClient
from pymongo import server_api
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os
from urllib.parse import quote_plus
from flask import jsonify

load_dotenv()
# Function to connect to MongoDB
def connect_to_mongodb():
    mongo_username = quote_plus(os.getenv('MONGO_USERNAME'))
    db_password = quote_plus(os.getenv('MONGO_PASSWORD'))
    db_name = os.getenv('DB_NAME')

    # MongoDB connection URI
    uri = f"mongodb+srv://{mongo_username}:{db_password}@news-analyzer.0ittn.mongodb.net/{db_name}?retryWrites=true&w=majority&appName=News-analyzer"
    client = MongoClient(uri, server_api=server_api.ServerApi('1'), ssl=True, tlsAllowInvalidCertificates=True)
    db = client[db_name]
    return db

def createURL(data):
    db=connect_to_mongodb()
    collection_name = os.getenv('COLLECTION_NAME')
    collection = db[collection_name]
    try :
        result = collection.insert_one(data)
        if not result :
            return jsonify({"error":"url not inserted"}),404
        return jsonify(result),200
    except Exception as e :
        return jsonify({"error" :str(e)}),500
    


def getURL(var):
    db=connect_to_mongodb()
    collection_name = os.getenv('COLLECTION_NAME')
    collection = db[collection_name]
    result = collection.find_one({'var':var})
    return result["url"]


        



