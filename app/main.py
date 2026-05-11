from fastapi import FastAPI
from pydantic import BaseModel

from app.chatbot import ask_chatbot
from app.guardrails import validate_input
from app.output_guardrails import validate_output


app = FastAPI()


# Request schema
class ChatRequest(BaseModel):
    question: str


# Home route
@app.get("/")
def home():

    return {
        "message": "LLM Chatbot API Running"
    }


# Chat route
@app.post("/chat")
def chat(request: ChatRequest):

    # -----------------------------
    # INPUT GUARDRAILS
    # -----------------------------

    input_validation = validate_input(request.question)

    # Block unsafe user input
    if not input_validation["safe"]:

        return {
            "blocked": True,
            "stage": "input_guardrails",
            "reason": input_validation["reason"]
        }

    # -----------------------------
    # ASK LLM
    # -----------------------------

    answer = ask_chatbot(request.question)

    # -----------------------------
    # OUTPUT GUARDRAILS
    # -----------------------------

    output_validation = validate_output(answer)

    # Block unsafe AI output
    if not output_validation["safe"]:

        return {
            "blocked": True,
            "stage": "output_guardrails",
            "reason": output_validation["reason"]
        }

    # -----------------------------
    # FINAL SAFE RESPONSE
    # -----------------------------

    return {
        "question": request.question,
        "answer": answer
    }