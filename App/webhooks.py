
from fastapi import FastAPI, Request, File, WebSocket, WebSocketDisconnect, UploadFile
import json
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse
from models import Question
from db import get_questions_by_email
from pydantic import BaseModel, EmailStr

email=None
class EmailRequest(BaseModel):
    email: str
    


app = FastAPI()
current_index = 0
def format_response(text):
    response = {
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": [text]
                        }
                    }
                ]
            }
    }

    return response

@app.get("/")
async def home(request:Request):
    return "ok"

@app.post("/post_email")
async def post_email(data: EmailRequest):
    """Receives email and session ID from interview API."""
    global email
    email = data.email    
    print(f"Email received: {email}")
    # You can store the data in a database or process it
    return {"message": "Data received successfully"}

questions = get_questions_by_email(email)





@app.post("/webhook")
async def handle_webhook(request: Request):

    global current_index

   

    body = await request.json()
    pretty_body = json.dumps(body, indent=4)

    page_info = body.get("pageInfo", {})
    session_info = body.get("sessionInfo", {})
    current_intent = session_info.get("parameters",{}).get("$request.generative.subIntent", "")
    current_page = page_info.get('displayName', "")

    if current_page == 'Entry Page' and current_intent == "":
        current_index = -1
        text = "Can you tell me about yourself?"
        current_index += 1
        response = format_response(text)

    elif current_page == "Entry Page" and current_intent == "answer":
        text = questions[current_index]
        current_index += 1
        response = format_response(text)

    elif current_page == "Entry Page" and current_intent == "repeat":
        if current_index == 0:
            text = "Can you tell me about yourself?"
        else:
            text = questions[current_index-1]
            
        response = format_response(text)

    elif current_page == "Entry Page" and current_intent == "skip":
        text = questions[current_index]
        current_index += 1
        response = format_response(text)

    elif current_page == "Entry Page" and current_intent == "exit":
        text = "Thank you for your time. Goodbye!"
        response = format_response(text)

    

    return JSONResponse(content=response, status_code=200)
