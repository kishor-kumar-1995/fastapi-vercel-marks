from fastapi import FastAPI, Request
from pydantic import BaseModel
import base64
import io
import openai
import os
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract

# Use AI Proxy endpoint and token
openai.api_base = "https://aiproxy.sanand.workers.dev/openai/v1"
openai.api_key = os.getenv("AIPROXY_TOKEN", "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZHMyMDAwMDE5QGRzLnN0dWR5LmlpdG0uYWMuaW4ifQ.YhuHaTceeOMovmnbt6Jdl-JLoZO-F47GVpednCJAgh8")

app = FastAPI()

# CORS settings (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model
class Query(BaseModel):
    question: str
    image: Optional[str] = None  # base64 string

# Output model
class Link(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[Link]

# Dummy link fetcher
def get_relevant_links(question: str):
    return [
        {
            "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/4",
            "text": "Use the model that’s mentioned in the question."
        },
        {
            "url": "https://discourse.onlinedegree.iitm.ac.in/t/ga5-question-8-clarification/155939/3",
            "text": "Tokenizer approach explained."
        }
    ]

# API endpoint
@app.post("/api/", response_model=AnswerResponse)
async def answer_question(query: Query):
    extracted_text = ""

    if query.image:
        try:
            image_data = base64.b64decode(query.image)
            image = Image.open(io.BytesIO(image_data))
            extracted_text = pytesseract.image_to_string(image)
        except Exception as e:
            extracted_text = f"[Image processing failed: {e}]"

    full_prompt = f"""
You are a Virtual TA for the IIT Madras Data Science program.

Student's question: {query.question}
Extracted text from image (if any): {extracted_text}

Please answer based on TDS 2025 Jan content and Discourse posts till 14 Apr 2025.
Only include direct and relevant answers. Avoid general replies.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful teaching assistant."},
            {"role": "user", "content": full_prompt}
        ]
    )

    answer = response['choices'][0]['message']['content']
    links = get_relevant_links(query.question)

    return {
        "answer": answer,
        "links": links
    }
