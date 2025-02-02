
# from pydantic import BaseModel
# from typing import List, Optional

# class QuestionSchema(BaseModel):
#     session_id: str  # Session ID
#     email: str  # New email field
#     jd_text: str  # Job description text
#     sample_questions: Optional[str] = None  # Optional sample questions
#     cv_content: str  # CV content extracted from the file
#     questions: List[str]  # List of generated questions
#     score: str  # Score of the CV
# class Question_AnswerSchema(BaseModel):
#     session_id: str  # Session ID
#     email: str  # New email field
#     questions: List[str]  # List of generated questions
#     Answers: List[str]  # List of generated answers

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChatSession(BaseModel):
    session_id: str
    
    user_response: Optional[str] = None
    bot_response: Optional[str] = None
    timestamp: datetime = datetime.utcnow()
class Question(BaseModel):

    email: str  # New email field
    jd_text: str  # Job description text
    sample_questions: Optional[str] = None  # Optional sample questions
    cv_content: str  # CV content extracted from the file
    questions: List[str]  # List of generated questions
    score: Optional[str] = None  # Score of the CV



