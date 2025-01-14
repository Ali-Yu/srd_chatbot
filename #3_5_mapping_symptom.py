import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_ENDPOINT = os.getenv("GROQ_API_ENDPOINT")
API_KEY = os.getenv("GROQ_API_KEY")

# Symptom类别的标准化词条列表
symptom_list = [
    "Aggressive behavior", "Avoidance behavior", "Compulsive checking", "Compulsive counting",
    "Compulsive ordering", "Compulsive washing and cleaning", "Demanding reassurance",
    "Down-turned corners of the mouth", "Following a strict routine", "Furrowed brows",
    "Increase in goal-directed activity", "Lack of facial expression", "Little body movement",
    "Morbid talkative", "Neglect personal hygiene", "Poor eye contact", "Restlessness",
    "Risk-taking behavior", "Self-destructive behavior", "Slumped posture", "Speech changes",
    "Aggressive or horrific thoughts about losing control and harming yourself or others",
    "Depersonalization", "Derealization", "Difficulty handling uncertainty",
    "Diminished ability to concentrate", "Diminished ability to think", "Distractibility",
    "Doubting and having a hard time dealing with uncertainty", "Fear of contamination or dirt",
    "Flight of ideas", "Inability to communicate", "Inability to set aside or let go of a worry",
    "Indecisiveness", "Memory problems, including not remembering important aspects of a traumatic event",
    "Mind going blank", "Needing things to be orderly and balanced",
    "Negative thoughts about yourself, other people or the world",
    "Overthinking plans and solutions to all possible worst-case outcomes",
    "Poor judgement", "Recurrent, involuntary, and intrusive distressing memories of the traumatic event(s)",
    "Repetitive negative thinking", "Trying not to think or talk about a traumatic event",
    "Unwanted thoughts, including aggression, or sexual or religious subjects",
    "Anxiety in anticipation of a feared activity or event", "Apathy symptom",
    "Avoidance of situations where you might be the center of attention", "Depressed mood",
    "Diminished interest or pleasure", "Emotional numbness", "Fear of death",
    "Fear of losing control", "Fear of physical symptoms that may cause you embarrassment",
    "Fear of situations in which you may be judged negatively", "Fear that others will notice that you look anxious",
    "Intense fear of interacting or talking with strangers", "Intense fear or anxiety during social situations",
    "Irritability", "Nervousness", "Nightmares about a traumatic event",
    "Ongoing negative emotions of fear, blame, guilt, anger or shame",
    "Persistent worrying or anxiety about a number of areas that are out of proportion to the impact of the events",
    "Sense of impending doom or danger", "Worry about embarrassing or humiliating yourself",
    "Delusions", "Dissociative reactions", "Flashbacks", "Hallucinations", "Abdominal Cramps",
    "Being easily fatigued", "Being easily startled", "blurred vision", "Blushing",
    "Burn of stomach", "Chest pain", "Chest tightness", "Chills", "Choking sensation",
    "Chronic pain", "Constipation", "Decreased Libido", "Decreased need for sleep",
    "Diarrhea", "Dizziness or lightheadedness", "Dry mouth", "Faint", "Fast heartbeat",
    "Fatigue", "Flatulence", "Frequent urination", "Headache", "Hot flashes",
    "Hypersomnia", "Indigestion", "Insomnia", "Irritable Bowel Syndrome", "Malnutrition",
    "Muscle tension", "Nausea", "Numbness", "Pain", "Palpitations",
    "Rapid breathing", "Sensations of shortness of breath", "Sleep disturbance",
    "Sweating", "Throat swelling", "Tingling sensations", "Trembling",
    "Unusual changes in appetite", "Unusual weight changes", "Urgency to urinate",
    "Vomiting", "Psychomotor agitation", "Psychomotor retardation",
    "Feelings of worthlessness", "Inappropriate guilt", "Inflated self-esteem",
    "Low self-esteem", "Refusal to acknowledge issues", "Feeling detached from family and friends",
    "Interpersonal Relationships", "Learning Capability", "Work Performance",
    "Always being on guard for danger", "Suicidal behavior", "Suicidal intent"
]

def map_symptom_terms(user_input):
    """
    Call the Groq API based on user input, mapping the input symptoms to standardized Symptom entries.
    """
    prompt = f"""
You are an expert in clinical psychology and mental health symptoms. Your task is to map the given input terms to standardized symptom names.

The input is a list of symptom-related terms. Compare each term with the standardized symptom list below and return only the matched terms from the list:

{', '.join(symptom_list)}

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
        response = requests.post(GROQ_API_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        mapped_terms = response_json['choices'][0]['message']['content'].strip()
        return mapped_terms if mapped_terms else "no mapping term"
    except Exception as e:
        print(f"Mapping error: {e}")
        return "no mapping term"


if __name__ == "__main__":
    user_input = "Depressed mood, Anxiety, poor sleep"
    mapped_terms = map_symptom_terms(user_input)
    print(f"Mapped Terms: {mapped_terms}")
