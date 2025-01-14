import os
import requests
from langdetect import detect, LangDetectException
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

GROQ_API_ENDPOINT = os.getenv("GROQ_API_ENDPOINT")
API_KEY = os.getenv("GROQ_API_KEY")

def translate_input(user_input):
    # 预处理：检查输入是否为空或只包含空白字符
    if not user_input.strip():
        print("Error: Input cannot be empty or only spaces.")
        return "Error: Input cannot be empty or only spaces."

    try:
        detected_lang = detect(user_input)
    except LangDetectException:
        print("Language detection failed: No features detected in text.")
        return "Error: Unable to detect language from input."

    if detected_lang == 'en':
        return user_input  # No translation needed

    prompt = f"""
Please translate the following text into English, return only the translated text, do not include any explanations, comments, or additional text:  
"{user_input}"  
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
        result = response_json['choices'][0]['message']['content'].strip() if 'choices' in response_json else user_input
        return result.replace('"', '')
    except Exception as e:
        print(f"Translation error: {e}")
        return "Error: Translation failed."
