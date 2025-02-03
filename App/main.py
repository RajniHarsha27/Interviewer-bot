from fastapi import FastAPI, Request, File, WebSocket, WebSocketDisconnect, UploadFile, Form
import json
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from google.cloud import dialogflowcx_v3 as dialogflow
import os
from dotenv import load_dotenv
from google.cloud import speech
from google.cloud import texttospeech
from typing import AsyncGenerator
import asyncio
import io
from fastapi.middleware.cors import CORSMiddleware
import uuid
from get_df_response import run_sample
from models import ChatSession
from pydantic import BaseModel, EmailStr
from db import candidate, interview_model
import httpx
import requests
from datetime import datetime

session_variables ={
    "user_email" : "",
    "valid" : False
}


env_path = "C:\Hubnex\Interviewer Assistant\.env"
load_dotenv(dotenv_path=env_path)

app = FastAPI()
print("Loaded credentials path:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

id_ = None

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})

class EmailValidationRequest(BaseModel):
    email: EmailStr  # Ensures valid email format

@app.post("/validate-email")
async def validate_email(request: Request, email: EmailStr = Form(...)):
    """Validates if the email exists in the database."""
    global session_variables
    print("email : ", email)
    existing_candidate = candidate.find_one({"email": email})
    if existing_candidate:
        session_variables["user_email"] = email
        session_variables["valid"] = True
        questions = candidate.find_one({"email": email}, {"_id": 0, "questions": 1})
        to_send = questions["questions"]
        async with httpx.AsyncClient() as client:
            response = await client.post("http://127.0.0.1:8001/send-questions/", json={"questions": to_send})
        print(response.json())

        return JSONResponse(content ={"message": "valid"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Invalid"}, status_code=400)
    

@app.get('/interview')
async def interview(request: Request):
    print("email inside interview route : ", session_variables["user_email"])
    if session_variables["valid"]:
        session_variables["valid"] = False
        return templates.TemplateResponse('interview.html', {'request': request, "var" : "variable"})
    else:
        return "access denied"


client = speech.SpeechClient()
def get_transcript(audio_content: bytes):
    # Prepare the audio for transcription without saving to a file
    audio = speech.RecognitionAudio(content=audio_content)
    
    # Define the configuration for the recognition request
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS, # Adjust this based on the actual sample rate
        language_code="en-US", 
        sample_rate_hertz=48000,
        audio_channel_count=1, # You can change the language code as needed
    )

    # Make the request to Google Cloud Speech-to-Text API
    response = client.recognize(config=config, audio=audio)

    print(response)

    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(f"Transcript: {result.alternatives[0].transcript}")
    
    # Return the transcriptions from the response
    return response.results

import time
def generate_audio(answer) -> bytes:
    """Synthesizes speech from the input string of ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/

    """
    print(answer)
    ssml = f"""<speak>{answer}</speak>"""
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(ssml=ssml)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Polyglot-1",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    return response.audio_content

    
def generate_df_answer(transcript) -> str:
    global id_
    answer = run_sample(transcript, id_)
    print("id : ", id_)
    return answer


@app.websocket("/ws/audio")
async def websocket_audio(websocket: WebSocket):
    global id_, session_variables
    await websocket.accept()
    
    #response = requests.post("http://127.0.0.1:8001/restart")
    #print("webhooks restarted")

    if id_ is None:
        id_ = str(uuid.uuid4())

    initial_response = run_sample("hi", id_)
    answer_audio = generate_audio(initial_response)
    await websocket.send_json({"answer" : initial_response})
    await websocket.send_bytes(answer_audio)
    first_user_response = True
    bot_response =[]
    
    try:
        while True:
            # Receive audio data as binary (audio file sent in chunks)
            audio_data = await websocket.receive_bytes()
            results = get_transcript(audio_data)
            transcript = " ".join([result.alternatives[0].transcript for result in results])

            if not first_user_response:
                user_response = transcript

            
            # Send the transcript back to the client
            await websocket.send_json({"transcript": transcript})
            
            answer = generate_df_answer(transcript) # fetches question from df webhook server
            bot_response.append(answer)
            

            if not first_user_response:
                document = {
                    "session_id" : id_,
                    "email" :session_variables["user_email"],
                    "bot_response" : bot_response[-2],
                    "user_response" : user_response,
                    "delivered_time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                }

                interview_model.insert_one(document)
                print("Data stored")

            first_user_response = False

            answer_audio = generate_audio(answer)
            await websocket.send_bytes(answer_audio)
            await websocket.send_json({"answer" : answer})

    except WebSocketDisconnect:
        print("Client disconnected.")


@app.get("/test")
async def test():
    path = os.path.join(os.getcwd(), 'sample.mp3')
    return str(path)