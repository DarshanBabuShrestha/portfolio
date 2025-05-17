from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import requests
import os

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API key from .env
load_dotenv()

# Global variable for storing uploaded text content
EXTRACTED_TEXT = """
Replace this with actual extracted text from a PDF or PPTX.
"""

@app.get("/")
def health_check():
    return {"message": "Chatbot backend is running."}

@app.post("/chat")
async def chat(query: str = Form(...)):
    global EXTRACTED_TEXT

    if not EXTRACTED_TEXT.strip():
        return JSONResponse(content={
            "response": "I don't have access to the course material. Please upload a PDF or PPTX first."
        })

    if not query.strip():
        return JSONResponse(content={"response": "Please ask a valid question."})

    gemini_api_url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        f"?key={os.getenv('GEMINI_API_KEY')}"
    )

    prompt = f"""
You are Darshan's AI assistant, trained exclusively on the content from Darshan Babu Shrestha’s portfolio website.

---

Darshan Babu Shrestha is a software engineer who thrives at the intersection of logic and creativity. He blends technical problem-solving with imaginative thinking to create meaningful and surprising experiences in tech.

He has worked on:
- AI Slide-to-Quiz Generator (Full-stack project using FastAPI, Gemini API, PDF/PPT parsing)
- GeminEye: an AI-powered real-time navigation system for visually impaired people (HackUTA Winner – Best Use of Gemini API)
- IBDP Grading Simulator Game in Python using Pygame
- CLI-based Java Stock Management System using OOP and file I/O
- Text-based Bingo game in C with random card generator and win detection

Skills/Tech Stack:
- Languages: Python, Java, C, JavaScript, HTML/CSS
- Frameworks/Libraries: FastAPI, PyMuPDF, python-pptx, OpenCV, Pygame
- APIs: Gemini API, Google Cloud Vision API, Google Text-to-Speech (TTS)
- Tools: GitHub

Internships (Summer 2025):
- Frontend Developer Intern @ GBCS Group (green-tech, fleet-based UI tools)
- Website Development Intern @ Tomorrow’s Leaders Today (TLT)
- Selected Scholar @ AI4ALL Ignite (AI ethics, mentorship, hands-on projects)

Certifications:
- IBM: Python for Data Science
- Google: Crash Course on Python
- UC Davis: SQL for Data Science
- University of Michigan: Python Data Structures & Programming for Everybody
- InSTEM Scholar at UTA

Philosophy:
Darshan describes himself as “split in half yet whole,” combining engineering precision with a creator's curiosity. He aims to build things that make people pause, smile, and think twice.

---

Your task is to:
- Answer only questions related to the above content in a friendly, helpful tone.
- If someone says "hello", "hi", or "how are you", reply politely and ask if they’d like to know more about Darshan.
- If someone asks a question that is unrelated to Darshan or the document, respond with:  
  **"I'm only here to answer questions about Darshan."**

**Question:** {query}
"""

    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(gemini_api_url, json=payload, headers=headers, timeout=15)
        response_data = response.json()

        if response.status_code == 200 and "candidates" in response_data:
            response_text = response_data["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            response_text = "I onlY tell you about Darshan."

    except Exception as e:
        print(f"Gemini API Error: {e}")
        response_text = "Error generating AI response."

    return JSONResponse(content={
        "response": response_text
    })
