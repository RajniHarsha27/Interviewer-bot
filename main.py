
from fastapi import FastAPI, UploadFile, Form,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from docx import Document
import PyPDF2 as pdf
from db import db
from models import QuestionSchema,Question_AnswerSchema
from pydantic import BaseModel
from bson import ObjectId

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
genai.configure(api_key="AIzaSyC1fxVBeFsISBwuvQXMN4ZjcW7UDKKNK1M")

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
    email: str = Form(...),  # New email field
    jd_text: str = Form(...),
    sample_questions: str = Form(""),
    cv_file: UploadFile = Form(...),
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
        questions = response.text.split("\n")[2:]

        # Save the data including email into MongoDB
        document = {
            "email": email,  # Save the email
            "jd_text": jd_text,
            "sample_questions": sample_questions,
            "cv_content": cv_content,
            "questions": questions,
        }
        await db.questions.insert_one(document)  # Save to the 'questions' collection

        return {"questions": questions}

    except Exception as e:
        return {"error": str(e)}



@app.get("/fetch-question/{email}/{index}")
async def fetch_question(email: str, index: int):
    try:
        # Query the MongoDB collection for documents with the specified email
        document = await db.questions.find_one({"email": email})

        # Check if the document is found
        if not document:
            raise HTTPException(status_code=404, detail="No records found for the provided email.")

        # Extract questions from the document
        questions = document.get("questions", [])

        # Check if the index is valid
        if index < 0 or index >= len(questions):
            raise HTTPException(status_code=400, detail="Invalid question index.")

        # Return the specific question
        return {
            "id": str(document["_id"]),  # Convert ObjectId to string for JSON serialization
            "email": document["email"],
            "question": questions[index],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
@app.get("/fetch-all-questions/{email}")
async def fetch_all_questions(email: str):
    try:
        # Query the MongoDB collection for documents with the specified email
        documents = await db.questions.find({"email": email}).to_list(length=100)

        # Check if any documents are found
        if not documents:
            raise HTTPException(status_code=404, detail="No records found for the provided email.")

        # Extract questions from the documents
        questions = []
        for document in documents:
            questions.extend(document.get("questions", []))

        return {"questions": questions}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
@app.post("/save-question-answers")
async def save_question_answers(data: Question_AnswerSchema):
    """
    Save email, questions, and answers into the 'question_answers' collection.

    Args:
        data (Question_AnswerSchema): The input data containing email, questions, and answers.

    Returns:
        dict: A success message with inserted document details.
    """
    try:
        # Convert the input Pydantic model to a dictionary
        document = data.model_dump()

        # Check if the number of questions matches the number of answers
        if len(document["questions"]) != len(document["Answers"]):
            raise HTTPException(
                status_code=400, detail="The number of questions and answers must match."
            )

        # Insert the document into the database
        result = await db.question_answers.insert_one(document)

        return {"message": "Data saved successfully.", "id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
