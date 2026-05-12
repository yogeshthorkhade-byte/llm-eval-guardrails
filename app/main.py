from fastapi import FastAPI

from fastapi import UploadFile

from fastapi import File

from pydantic import BaseModel

import shutil

from app.chatbot import ask_chatbot

from app.guardrails import validate_input

from app.output_guardrails import validate_output

from app.faithfulness import (
    evaluate_faithfulness
)

from app.document_manager import (
    add_document
)


# --------------------------------
# FastAPI App
# --------------------------------

app = FastAPI()


# --------------------------------
# Request Schema
# --------------------------------

class ChatRequest(BaseModel):

    question: str


# --------------------------------
# Home Route
# --------------------------------

@app.get("/")

def home():

    return {

        "message":
            "LLM Evaluation & Guardrails API"
    }


# --------------------------------
# Chat Route
# --------------------------------

@app.post("/chat")

def chat(request: ChatRequest):

    # --------------------------------
    # Input Guardrails
    # --------------------------------

    input_check = validate_input(
        request.question
    )


    if not input_check["safe"]:

        return {

            "blocked": True,

            "stage": "input_guardrails",

            "reason": input_check[
                "reason"
            ]
        }


    # --------------------------------
    # Ask RAG Chatbot
    # --------------------------------

    response = ask_chatbot(
        request.question
    )


    # --------------------------------
    # Faithfulness Evaluation
    # --------------------------------

    faithfulness = (
        evaluate_faithfulness(

            response["answer"],

            response["sources"]

        )
    )


    # --------------------------------
    # Output Guardrails
    # --------------------------------

    output_check = validate_output(
        response["answer"]
    )


    if not output_check["safe"]:

        return {

            "blocked": True,

            "stage": "output_guardrails",

            "reason": output_check[
                "reason"
            ]
        }


    # --------------------------------
    # Final Response
    # --------------------------------

    return {

        "question": request.question,

        "answer": response["answer"],

        "sources": response["sources"],

        "faithfulness_score":
            faithfulness[
                "faithfulness_score"
            ],

        "hallucination_detected":
            faithfulness[
                "hallucination_detected"
            ]
    }


# --------------------------------
# Upload PDF Endpoint
# --------------------------------

@app.post("/upload-pdf")

def upload_pdf(
    file: UploadFile = File(...)
):

    # Save uploaded file
    file_path = f"data/{file.filename}"


    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    # Add document to vector DB
    result = add_document(
        file_path
    )


    return {

        "filename": file.filename,

        "status": result
    }