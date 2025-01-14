import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_ENDPOINT = os.getenv("GROQ_API_ENDPOINT")
API_KEY = os.getenv("GROQ_API_KEY")

# RiskFactor类别的标准化词条列表
riskfactor_list = [
    "Chronic or disabling medical conditions", "Incomplete inter-episode recovery", "Major nonmood disorders",
    "Substance use, anxiety, and borderline personality disorders", "Cultural differences",
    "Do not have a good support system of family and friends", "Exposure to repeated upsetting reminders",
    "High income country", "Lower education", "Major changes in life", "Negative experiences",
    "New social or work demands", "Physical and sexual abuse in childhood",
    "Separated, Divorced, Or Widowed Status", "Stressful life events", "Trauma-related losses",
    "Traumatic event", "Early-onset and recurrent forms", "Family history",
    "First-degree family members", "Gender-related features", "Shared genetic origin with schizophrenia",
    "Significant genetic predisposition", "Alcohol", "Autoimmune syndrome", "Being a perpetrator",
    "Being threatened with a weapon", "Combat exposure", "Corticosteroids", "Excessive caffeine intake",
    "Having an appearance or condition that draws attention", "Perceived life threat", "Physical assault",
    "Sexual violence", "Smoking", "Were physically injured during the traumatic event", "Witnessing atrocities",
    "Anxiety sensitivity", "Behavioral inhibition", "Development of acute stress disorder",
    "Fear of negative evaluation", "Greater internalizing symptoms", "Harm avoidance",
    "Higher negative emotionality", "Inappropriate coping strategies", "Negative appraisals",
    "Neuroticism (negative affectivity)"
]

def map_riskfactor_terms(user_input):
    """
    Call the Groq API based on user input, mapping the input risk factors to standardized RiskFactor entries.
    """
    # 优化后的Prompt
    prompt = f"""
You are an expert in psychological and physiological risk factors. Your task is to map the given input terms to standardized risk factor names.

The input is a list of risk factor-related terms. Compare each term with the standardized risk factor list below and return only the matched terms from the list:

{', '.join(riskfactor_list)}

If none of the input terms match any terms from the list, return only 'no mapping term'. Do not create new terms or modify existing ones.

### Input:
{user_input}

### Output:
- Return only the matched terms exactly as they appear in the list, separated by commas.
- Do not include any explanations, comments, or additional text.
- Ensure consistency in the format across all responses, regardless of the input or conversation history.
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
        # 向API发送请求
        response = requests.post(GROQ_API_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        # 获取API响应结果并去除多余的空白
        mapped_terms = response_json['choices'][0]['message']['content'].strip()
        
        # 如果有映射结果，返回它们
        return mapped_terms if mapped_terms else "no mapping term"
    except Exception as e:
        print(f"Mapping error: {e}")
        return "no mapping term"


if __name__ == "__main__":
    # 示例输入
    user_input = "Long-term heavy drinking"
    mapped_terms = map_riskfactor_terms(user_input)
    print(f"Mapped Terms: {mapped_terms}")
