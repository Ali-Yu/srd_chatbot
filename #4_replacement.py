import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_ENDPOINT = os.getenv("GROQ_API_ENDPOINT")
API_KEY = os.getenv("GROQ_API_KEY")

def replace_with_mapped_terms(original_text, mapped_terms):
    if "no mapping term" in mapped_terms.lower():
        return original_text

    prompt = f"""
    Please replace any non-standard terms with their corresponding standardized terms.
    Here is the original text:
    "{original_text}"

    Below is the list of standardized terms:
    {mapped_terms}

    Please identify any concepts in the original text that correspond to the standardized terms and replace them accordingly, leaving the rest of the text unchanged.
    Only return the full text with the replacements. Do not include any extra text or explanations in the output.
    """

    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama3-70b-8192"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    try:
        response = requests.post(GROQ_API_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        return response_json['choices'][0]['message']['content'] if 'choices' in response_json else original_text
    except Exception as e:
        print(f"Replacement error: {e}")
        return original_text
