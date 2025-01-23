

from fastapi import FastAPI,Request, jsonify
from typing import Dict, Any
from pydantic import BaseModel

class SessionInfo(BaseModel):
    session: str
    parameters: Dict[str, Any] = {}

class FulfillmentInfo(BaseModel):
    tag: str

class WebhookRequest(BaseModel):
    fulfillmentInfo: FulfillmentInfo
    sessionInfo: SessionInfo

class TextResponse(BaseModel):
    text: str

class FulfillmentResponse(BaseModel):
    messages: list[TextResponse]

class WebhookResponse(BaseModel):
    fulfillmentResponse: FulfillmentResponse
    sessionInfo: SessionInfo = None

app = FastAPI()

@app.get('/')
async def name(request: Request):
    return "ok"

@app.post('/webhook')
async def handle_webhook(request: WebhookRequest):
    req = await request.model_dump_json()
    webhook_request = WebhookRequest(**req)

    return jsonify


