from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from pdfminer.high_level import extract_text
from typing import Optional

app = FastAPI()

class ArxivLink(BaseModel):
    url: str

class SummaryRequest(BaseModel):
    pdf_url: str

class LinkedInPostRequest(BaseModel):
    summary: str

@app.post("/download_pdf")
async def download_pdf(arxiv_link: ArxivLink):
    try:
        response = requests.get(arxiv_link.url)
        response.raise_for_status()
        pdf_content = response.content
        return {"pdf_content": pdf_content}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate_summary")
async def generate_summary(request: SummaryRequest):
    try:
        response = requests.get(request.pdf_url)
        response.raise_for_status()
        pdf_content = response.content
        text = extract_text(pdf_content)
        summary = summarize_text(text)
        return {"summary": summary}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/create_linkedin_post")
async def create_linkedin_post(request: LinkedInPostRequest):
    summary = request.summary
    linkedin_post = generate_linkedin_post(summary)
    return {"linkedin_post": linkedin_post}

def summarize_text(text: str) -> str:
    # Placeholder function for summarizing text
    return "This is a summary of the PDF content."

def generate_linkedin_post(summary: str) -> str:
    # Placeholder function for generating LinkedIn post
    return f"Check out this summary: {summary}"
