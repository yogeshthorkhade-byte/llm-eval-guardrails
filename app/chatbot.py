from groq import Groq
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Read API key
api_key = os.getenv("GROQ_API_KEY")

# Create Groq client
client = Groq(api_key=api_key)


def ask_chatbot(question: str):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = response.choices[0].message.content

    return answer