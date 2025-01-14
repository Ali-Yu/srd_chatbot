import os
import requests
from dotenv import load_dotenv
import json

# 加载环境变量
load_dotenv()

# API 配置
GROQ_API_ENDPOINT = os.getenv("GROQ_API_ENDPOINT")
API_KEY = os.getenv("GROQ_API_KEY")


def classify_input(user_input):
    """
    Send user input to the LLM and return the classification results.
    """
    prompt = f"""
    You are tasked with extracting and classifying keywords explicitly mentioned in the input. 
    Focus only on exact matches and classify them into the following categories:
    - Disorder
    - Biomarker
    - Measurement
    - RiskFactor
    - Symptom
    - Treatment

    Rules:
    - Do not infer or add keywords beyond the input.
    - If the keyword matches a category, ignore the keyword.
    - Return a valid JSON object containing only detected categories and exact keywords.

    Input: {user_input}
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(GROQ_API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("choices", [])[0].get("message", {}).get("content", "{}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "{}"



