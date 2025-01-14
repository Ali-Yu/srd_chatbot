import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
GROQ_API_ENDPOINT = os.getenv("GROQ_API_ENDPOINT")
API_KEY = os.getenv("GROQ_API_KEY")

def is_mental_health_related(user_input):
    """
    判断用户输入是否与心理健康相关。
    
    参数：
    - user_input (str): 用户输入的文本。
    
    返回值：
    - bool: 如果与心理健康相关，返回 True；否则返回 False。
    """
    # 提问给 LLM 的 prompt
    prompt = f"""
You are an expert in psychology, psychiatry, cognitive science, and neuroscience. 
Your task is to determine whether the given input is related to the field of mental health. 
Provide only "Yes" or "No" as the answer without explanations, comments, or additional text.

Input: "{user_input}"
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
        # 请求 LLM 接口
        response = requests.post(GROQ_API_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        result = response_json['choices'][0]['message']['content'].strip()

        # 根据 LLM 返回的结果判断
        return result.lower() == "yes"
    except Exception as e:
        print(f"Error during topic classification: {e}")
        return False

# 测试代码
if __name__ == "__main__":
    test_input = "今天天气如何？"
    
    result = is_mental_health_related(test_input)
    
    # 仅输出 "yes" 或 "no"
    print("yes" if result else "no")
