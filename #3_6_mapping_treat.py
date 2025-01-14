import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_ENDPOINT = os.getenv("GROQ_API_ENDPOINT")
API_KEY = os.getenv("GROQ_API_KEY")

# Treatment类别的标准化词条列表
treatment_list = [
    "Herbal products", "Omega-3 fatty acids", "Oryzanol tablets", "Prebiotic supplementation", "Aromatherapy",
    "Biofeedback, Psychology", "Hypnosis", "Meditation", "Qigong", "Tai Ji", "Yoga",
    "Mindfulness-Based Cognitive Therapy", "Mindfulness-Based Stress Reduction", "40 Hz Sensory Therapy",
    "Horticultural Therapy", "Dance Therapy", "Drawing Therapy", "Music Therapy", "Poetry Therapy",
    "Exercise Therapy", "Atypical Antidepressants", "Monoamine Oxidase Inhibitors",
    "Noradrenergic and Specific Serotonergic Antidepressants", "Selective Serotonin Reuptake Inhibitors",
    "Serotonin and Norepinephrine Reuptake Inhibitors", "Serotonin modulators", "Tricyclic Antidepressants",
    "Benzodiazepines", "Non-benzodiazepines", "Androgens", "Estrogen", "Thyroid Hormones", "Ketamine",
    "Prazosin", "Stellate ganglion block", "Antipsychotics", "Hypnotics and Sedatives", "Mood Stabilizers",
    "β-Blockers", "Electroconvulsive Therapy", "Transcranial Direct Current Stimulation",
    "Deep brain stimulation", "Transcranial Magnetic Stimulation", "Acceptance and Commitment Therapy",
    "Cognitive Restructuring", "Exposure Therapy", "Dialectical Behavior Therapy",
    "Eye movement desensitization and reprocessing therapy", "Interpersonal therapy"
]

def map_treatment_terms(user_input):
    """
    Call the Groq API based on user input, mapping the input treatment methods to standardized Treatment entries.
    """
    # 优化后的Prompt
    prompt = f"""
You are an expert in treatment methods for mental health disorders. Your task is to map the given input terms to standardized treatment names.

The input is a list of treatment-related terms. Compare each term with the standardized treatment list below and return only the matched terms from the list:

{', '.join(treatment_list)}

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
    user_input = "Cognitive Behavioral Therapy"
    mapped_terms = map_treatment_terms(user_input)
    print(f"Mapped Terms: {mapped_terms}")
