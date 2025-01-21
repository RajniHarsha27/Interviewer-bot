from pydantic import BaseModel
from typing import List, Optional

class QuestionSchema(BaseModel):
    jd_text: str  # Job description text
    sample_questions: Optional[str] = None  # Optional sample questions
    cv_content: str  # CV content extracted from the file
    questions: List[str]  # List of generated questions
