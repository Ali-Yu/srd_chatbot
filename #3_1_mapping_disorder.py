import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_ENDPOINT = os.getenv("GROQ_API_ENDPOINT")
API_KEY = os.getenv("GROQ_API_KEY")

# Disorder类别的标准化词条列表
disorder_list = [
    "Major Depressive Disorder", "Bipolar Disorder", "Obsessive-Compulsive Disorder", "Posttraumatic Stress Disorder", 
    "Generalized Anxiety Disorder", "Panic Disorder", "Social Anxiety Disorder", "Depressive Disorder", 
    "Substance Use Disorder", "Attention-Deficit Hyperactivity Disorder (ADHD)", "Separation Anxiety Disorder", 
    "Specific Phobia", "Agoraphobia", "Avoidant Personality Disorder", "Borderline Personality Disorder", 
    "Antisocial Personality Disorder", "Psychotic Disorder", "Eating Disorders", "Anorexia Nervosa", "Bulimia Nervosa", 
    "Dysthymia", "Body Dysmorphic Disorder", "Tic Disorder", "Trichotillomania", "Excoriation (Skin-Picking) Disorder", 
    "Tourette's Disorder", "Substance/Medication-Induced Disorder", "Substance/Medication-Induced Bipolar Disorder", 
    "Acute Stress Disorder", "Illness Anxiety Disorder", "Conduct Disorder", "Conversion Disorder", "Mild Traumatic Brain Injury", 
    "Traumatic Brain Injury", "Schizophrenia", "Schizoaffective Disorder", "Obsessive-Compulsive Personality Disorder (OCPD)", 
    "Hikikomori", "High-Functioning Autism (in children)", "Selective Mutism (in children)", "Normative Shyness", 
    "Anxiety Disorders", "Personality Disorders", "Suicidal Thoughts or Suicide", "Phobias", "Adjustment Disorder", 
    "Chronic Obstructive Pulmonary Disease", "Epilepsy", "Hyperthyroidism", "Pheochromocytoma", "Transient Ischemic Attack", 
    "Angina", "Asthma", "Congestive Heart Failure", "Mitral Valve Prolapse", "Pulmonary Embolism", "Delusional Disorder", 
    "Schizoid Personality Disorder", "Substance-Related Disorder", "Hoarding Disorder", "Dissociative Disorders", 
    "Irritable Bowel Syndrome", "Mild Alcohol Use Disorder", "Major Neurocognitive Disorder"
]


def map_disorder_terms(user_input):
    """
    Call the Groq API based on user input, mapping the input symptoms or diseases to standardized Disorder entries.
    """
    # 优化后的Prompt
    prompt = f"""
You are an expert in mental health. Your task is to map the given input terms to standardized disorder names.

The input is a list of disorder-related terms. Compare each term with the standardized disorder list below and return only the matched terms from the list:

{', '.join(disorder_list)}

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
    user_input = "Alzheimer's Disease"
    mapped_terms = map_disorder_terms(user_input)
    print(f"Mapped Terms: {mapped_terms}")
