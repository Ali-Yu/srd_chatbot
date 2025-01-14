import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_ENDPOINT = os.getenv("GROQ_API_ENDPOINT")
API_KEY = os.getenv("GROQ_API_KEY")

# Measurement类别的标准化词条列表
measurement_list = [
    "Behavioral Approach Test", "Attentional blink task", "Choice reaction time task", "Eye Tracking Tasks",
    "Face-in-the-crowd task", "Psychomotor Vigilance Task", "Dot Probe Task", "The auditory mismatch negativity",
    "Wisconsin Card Sorting Test", "Electroencephalography", "Iowa Gambling Task", "Emotional Face Processing",
    "Wall of Faces", "Emotional Go/No-Go task", "Emotional Stroop Task", "Antisaccade Task",
    "Conditioned Fear Acquisition and Generalization", "Skin conductance response", "Startle Response",
    "Go/No-Go Task", "Stroop Task", "Cyberballs", "Fear conditioning and extinction", "Delay discounting task",
    "Stop-signal task", "Probabilistic object reversal task", "Monetary and social incentive delay task",
    "Self-Report Public Speaking Task", "Self-referential memory task", "Theory of Mind Tasks", "Social reward task",
    "Cold Pressor Test", "Heart Rate Variability", "Trier Social Stress Test", "Carbon dioxide challenge test",
    "California Verbal Learning Test", "N-back task", "Beck Anxiety Inventory", "Hamilton Anxiety Rating Scale",
    "State-Trait Anxiety Inventory", "Anxiety Sensitivity Index", "Body Sensations Questionnaire",
    "Agoraphobic Cognitions Questionnaire", "Cognitive Failures Questionnaire", "Ecological momentary assessment",
    "Positive and Negative Affect Schedule", "Fear Questionnaire", "Spence Children's Anxiety Scale",
    "Childhood Trauma Questionnaire", "Life Events and Difficulties Schedule", "Life Events Checklist",
    "Barratt Impulsiveness Scale", "Intolerance of Uncertainty Scale-12", "Parental Bonding Instruments",
    "Scale for the Assessment of Negative Symptoms", "Scale for the Assessment of Positive Symptoms",
    "Symptom Checklist-90-Revised", "PTSD Checklist", "Thought Action Fusion Questionnaire",
    "Beck Hopelessness Scale", "Hamilton Depression Rating Scale", "Fatigue Severity Scale",
    "Child Obsessive-Compulsive Impact Scale", "Obsessive-Compulsive Inventory", "Padua Inventory",
    "Yale-Brown Obsessive Compulsive Scale", "Panic Disorder Severity Scale", "Insomnia Severity Index",
    "Pittsburgh Sleep Quality Index", "Fear of negative evaluation", "Liebowitz Social Anxiety Scale",
    "Social Anhedonia scale", "Social Phobia Inventory", "Multidimensional Scale of Perceived Social Supports"
]


def map_measure_terms(user_input):
    """
    Call the Groq API based on user input, mapping the input measurement tools to standardized Measurement entries.
    """
    # 优化后的Prompt
    prompt = f"""
You are an expert in psychological and physiological measurement tools. Your task is to map the given input terms to standardized measurement names.Be cautious of common measurement abbreviations, as they might overlap with terms from other domains. Ensure precise mapping to the correct standardized measurement names.

The input is a list of measurement-related terms. Compare each term with the standardized measurement list below and return only the matched terms from the list:

{', '.join(measurement_list)}

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