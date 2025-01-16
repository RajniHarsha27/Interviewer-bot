questions = ['Your CV highlights experience with various LLMs and NLP tasks. Can you describe a project where you had to fine-tune a large language model for a specific application, detailing the challenges you faced and how you overcame them?',
 'The job description emphasizes experience with RAG (Retrieval-Augmented Generation).  Describe your experience building and deploying RAG systems. What were some key design decisions you made, and what were the performance implications of those choices?',
 "You've worked with both TensorFlow and PyTorch.  Can you compare and contrast your experiences with these frameworks, particularly in the context of LLM development and deployment?  Which would you choose for a specific task and why?",
 'This role requires collaboration with instructional designers.  Describe a situation where you successfully collaborated with a non-technical team to achieve a shared goal. What communication strategies did you employ?',
 'The job description mentions developing metrics to evaluate LLM performance. What metrics would you use to assess the effectiveness of an AI tutor, and how would you interpret those metrics to inform model improvements?',
 'You mention experience with Flask and FastAPI.  What are the trade-offs between these frameworks, and which would you choose for building the backend services for our AI tutors, and why?',
 'Explain your understanding of MLOps and DevOps, and how these practices would apply to the continuous improvement and deployment of our AI language learning tutors.',
 'Describe your experience with A/B testing in the context of machine learning models.  How would you design an A/B test to compare different LLM architectures or prompt engineering strategies for our AI tutors?',
 'Our AI tutors need to be emotionally intuitive. How would you approach designing and implementing this aspect of the AI, considering the limitations and ethical considerations of current LLM technology?',
 'The job description mentions staying updated with the latest advancements in LLM technologies.  What are some recent advancements in LLMs that you find particularly exciting, and how do you keep yourself informed about these developments?']

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


