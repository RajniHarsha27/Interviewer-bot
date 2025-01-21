from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import google.generativeai as genai
from docx import Document
import PyPDF2 as pdf
from src.db import db
from src.models import QuestionSchema

# Initialize FastAPI
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Utility functions for file content extraction
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def input_docx_text(uploaded_file):
    doc = Document(uploaded_file.file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

@app.post("/generate-questions")
async def generate_questions(
    jd_text: str = Form(...),
    sample_questions: str = Form(""),
    cv_file: UploadFile = Form(...)
):
    try:
        # Read and process the CV file content
        if cv_file.content_type == "application/pdf":
            cv_content = input_pdf_text(cv_file)
        elif cv_file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            cv_content = input_docx_text(cv_file)
        elif cv_file.content_type == "text/plain":
            cv_content = await cv_file.read()
            cv_content = cv_content.decode("utf-8")
        else:
            return {"error": "Unsupported file format. Upload a TXT, PDF, or DOCX file."}

        if not cv_content.strip():
            return {"error": "The uploaded CV file is empty."}

        # Generate questions using Generative AI
        prompt = f"""
        You are a highly experienced Recruitment Specialist and Interview Strategist with expertise in 
creating tailored interview questions for a wide range of roles and industries. Your task is to 
generate a list of **10 customized interview questions** for a specific job candidate based on 
the provided **Job Description**, their **CV**, and a set of **Sample Questions** for reference.
Key areas to focus on:
1. **Relevance to Job Description**: The questions should target the essential skills, 
responsibilities, and expectations outlined in the job description.
2. **Candidate-Specific Tailoring**: The questions must delve deeper into the candidate's 
professional experience, achievements, skills, and qualifications mentioned in their CV.
3. **Inspiration from Sample Questions**: Use the provided sample questions as a baseline to 
craft high-quality, insightful queries.
4. **Competency Assessment**: Include questions that evaluate the candidate's:
   - Technical expertise and problem-solving abilities.
   - Soft skills and behavioral traits (e.g., teamwork, leadership, adaptability).

    - Alignment with the job’s responsibilities and organizational values.
Output format:
- Provide the questions in a numbered list, ensuring a balance of open-ended and scenario-
based questions.
- Include questions that can help assess the candidate’s depth of expertise, approach to 
challenges, and potential fit for the role.

Input Details:
        Job Description: {jd_text}
        Candidate CV: {cv_content}
        Sample Questions: {sample_questions}

Please generate questions that offer detailed insights into the candidate’s suitability for the role 
and help interviewers make informed decisions.
        """
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        questions = response.text.split("\n")

        # Save the data into MongoDB
        document = {
            "jd_text": jd_text,
            "sample_questions": sample_questions,
            "cv_content": cv_content,
            "questions": questions,
        }
        await db.questions.insert_one(document)  # Save to the 'questions' collection

        return {"questions": questions}

    except Exception as e:
        return {"error": str(e)}
