from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

PROJECT_ID = "animedevta-fsdf"
LANGUAGE_CODE = "en"
SERVICE_ACCOUNT_FILE = "./animedevta-fsdf-2ccb0169860c.json"
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text

@app.post("/api/chatbot")
async def chatbot_endpoint(request: ChatRequest):
    user_query = request.query
    session_id = str(uuid.uuid4())  
    bot_response = detect_intent_texts(PROJECT_ID, session_id, user_query, LANGUAGE_CODE)

    return {"response": bot_response}
