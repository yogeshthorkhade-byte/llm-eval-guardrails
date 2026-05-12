import os

from groq import Groq

from dotenv import load_dotenv

from app.rag import get_relevant_context

from app.memory import (
    add_to_memory,
    get_memory
)


# --------------------------------
# Load Environment Variables
# --------------------------------

load_dotenv()


# --------------------------------
# Initialize Groq Client
# --------------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# --------------------------------
# Ask Chatbot
# --------------------------------

def ask_chatbot(question):

    # --------------------------------
    # Retrieve Context
    # --------------------------------

    try:

        context, sources = (
            get_relevant_context(question)
        )

    except:

        context = ""

        sources = []


    # --------------------------------
    # Get Conversation Memory
    # --------------------------------

    memory = get_memory()


    # --------------------------------
    # Detect Whether RAG Is Useful
    # --------------------------------

    use_rag = False


    if context and len(sources) > 0:

        top_score = sources[0]["score"]


        # Lower score = better semantic match
        if top_score < 1.5:

            use_rag = True


    # --------------------------------
    # Dynamic System Prompt
    # --------------------------------

    if use_rag:

        system_prompt = f"""
        You are an intelligent AI assistant.

        Use the provided document context
        whenever it is relevant.

        If the question is unrelated to the
        document, answer naturally using
        your own knowledge.

        DOCUMENT CONTEXT:

        {context}
        """

    else:

        system_prompt = """
        You are a helpful AI assistant.

        Answer naturally, clearly,
        and professionally.

        Keep responses concise and accurate.
        """


    # --------------------------------
    # Build Messages
    # --------------------------------

    messages = [

        {
            "role": "system",
            "content": system_prompt
        }
    ]


    # Add memory
    messages.extend(memory)


    # Add user message
    messages.append(

        {
            "role": "user",
            "content": question
        }
    )


    # --------------------------------
    # Streaming Response
    # --------------------------------

    stream = (
        client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=messages,

            temperature=0.4,

            max_tokens=1024,

            stream=True
        )
    )


    answer = ""


    for chunk in stream:

        content = (
            chunk.choices[0]
            .delta.content
        )


        if content:

            answer += content


    # --------------------------------
    # Store Memory
    # --------------------------------

    add_to_memory(
        "user",
        question
    )


    add_to_memory(
        "assistant",
        answer
    )


    return {

        "answer": answer,

        "sources": sources
    }