# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 16:51:32 2025

"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the fine-tuned model
sentiment_pipeline = pipeline("text-classification", model="Wenfi/fine-tuned-DistilBert_Xu")

# Define request format
class SentimentRequest(BaseModel):
    text: str
    model: str  # Either "custom" or "llama"

def analyze_with_llama(text):
    api_url = "https://api.groq.com/openai/v1/chat/completions"  

    headers = {
        "Authorization": "Bearer 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",     
        "Content-Type": "application/json"
    }
    prompt = f"Classify the sentiment of this text as positive or negative:\n'{text}'"
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(api_url, json=payload, headers=headers)

    # Debugging print statements
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    if response.status_code == 200:
        result = response.json()
        sentiment = result['choices'][0]['message']['content'].strip().lower()
        confidence = 0.9  # Placeholder confidence score
        return sentiment, confidence
    else:
        raise HTTPException(status_code=500, detail=f"Llama model failed: {response.text}")

@app.post("/analyze/")
def analyze_sentiment(request: SentimentRequest):
    if request.model == "custom":
        result = sentiment_pipeline(request.text)[0]
        return {"sentiment": result["label"], "confidence": result["score"]}
    
    elif request.model == "llama":
        sentiment, confidence = analyze_with_llama(request.text)
        return {"sentiment": sentiment, "confidence": confidence}

    else:
        raise HTTPException(status_code=400, detail="Invalid model. Use 'custom' or 'llama'.")
