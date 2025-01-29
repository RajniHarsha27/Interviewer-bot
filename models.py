from pydantic import BaseModel
from typing import List, Optional

class QuestionSchema(BaseModel):
    email: str  # New email field
    jd_text: str  # Job description text
    sample_questions: Optional[str] = None  # Optional sample questions
    cv_content: str  # CV content extracted from the file
    questions: List[str]  # List of generated questions

class Question_AnswerSchema(BaseModel):
    email: str  # New email field
    
    questions: List[str]  # List of generated questions
    Answers: List[str]  # List of generated answers

