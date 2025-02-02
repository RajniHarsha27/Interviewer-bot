from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

env_path = "C:\Hubnex\Interviewer Assistant\.env"
load_dotenv(dotenv_path=env_path)

password = os.environ.get('MONGODB_PASSWORD')
print(password)


uri = f"mongodb+srv://hubnex:{password}@cluster0.v9ryx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.hubnex
candidate = db["candidate_data"]

