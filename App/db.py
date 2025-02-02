from pymongo import MongoClient
import os
from dotenv import load_dotenv
from models import ChatSession

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client.hubnexdb
collection = db["chat_sessions"]
questions_collection=db["questions"]
def store_chat(session_id: str, email:str,user_response: str = None, bot_response: str = None):
    """Stores user and bot responses in the database."""
    chat_entry = {
        "session_id": session_id,
        "email":email,
        "user_response": user_response,
        "bot_response": bot_response
    }
    collection.insert_one(chat_entry)

def get_questions_by_email(email: str):
    """Fetches questions based on the provided email ID."""
    questions = questions_collection.find_one({"email": email})
    if questions:
        return questions.get("questions", [])
    return []

def check_email_exists(email: str) -> bool:
    """Checks if the given email exists in the database."""
    user = questions_collection.find_one({"email": email})
    return bool(user)