from fastapi import FastAPI, UploadFile, Form,HTTPException, Request, File
from fastapi.middleware.cors import CORSMiddleware
from db import candidate
from generate_question import generate_questions
from docx import Document
import PyPDF2 as pdf
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse('portal.html', {'request': request})

@app.post("/upload")
async def upload(
    jd: str = Form(...,min_length=50),
    sample_questions: str = Form(""),
    cv: UploadFile = File(...),
    name: str = Form(...),
    email: EmailStr = Form(...)
):
    existing_candidate = candidate.find_one({"email": email})

    if existing_candidate:
        return {
            "message": "A candidate with this email already exists.",
            "error": "Email id already present"
        }

    cv_content = input_pdf_text(cv)
    questions = generate_questions(cv_content, jd, sample_questions)

    document = {
        "name": name,
        "email": email,
        "jd": jd,
        "cv_filename": cv_content,
        "questions": questions,
    }

    try :
        insert_result = candidate.insert_one(document)
        message = "Data inserted successfully."
        err = "no error"
    except Exception as e:
        message = "Error while inserting data to the database."
        err = str(e)

    return {
        "message" : message,
        "error" : err
    }

