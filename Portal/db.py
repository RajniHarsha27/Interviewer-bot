from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
env_path = r"C:\Hubnex\Interviewer Assistant\.env"  # Ensure correct path
load_dotenv(dotenv_path=env_path)

password = os.environ.get('MONGODB_PASSWORD')
if not password:
    raise ValueError("MONGODB_PASSWORD not found in environment variables")

# MongoDB URI
uri = f"mongodb+srv://hubnex:{password}@cluster0.v9ryx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Async MongoDB Client
client = AsyncIOMotorClient(uri)

# Database & Collection
db = client.hubnex
candidate = db["candidate_data"]
