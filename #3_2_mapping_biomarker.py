import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_ENDPOINT = os.getenv("GROQ_API_ENDPOINT")
API_KEY = os.getenv("GROQ_API_KEY")

# Biomarker类别的标准化词条列表
biomarker_list = [
    "Dopaminergic neurons", "Endomannosidase gene", "Fibroblasts", "GABAergic cells", "Glia cells",
    "Granule cell", "Hippocampal neurons", "Layer III pyramidal cells", "Microglia", "Microglia-like cells",
    "Noradrenergic neurons", "Oxytocin neurons", "Parvalbumin", "Pontine locus coeruleus astrocytes",
    "Prefrontal cortical neurons", "Red blood cell", "ACC directional signaling shift", "Amygdala activity",
    "Amygdala connectivity", "Amygdala volume and structure",
    "Anterior cingulate cortex (ACC) and anterior insula (AI) connectivity",
    "Anterior cingulate cortex function", "Anterior cingulate cortex structure", "Attention Network",
    "Autonomic Nervous System", "Basal Ganglia Alterations", "Basolateral amygdala connectivity",
    "Bed nucleus of stria terminalis", "Bilateral insula function", "Cerebello-cerebral Functional Connectivity",
    "Cortico-striato-thalamo-cortical", "Default mode network", "Dorsal anterior cingulate cortex interactions",
    "Dorsal anterior cingulate cortex lactate levels", "Dorsolateral Prefrontal Cortex connectivity",
    "Executive function circuitry", "Fronto-amygdala connectivity", "Hippocampal function",
    "Hippocampus volume and structure", "HPA axis", "Insula functional connectivity", "Insula volume and structure",
    "Insular Subregions", "lateral habenula", "lateral hypothalamus - medial forebrain bundle", "Lateral septum",
    "Medial prefrontal cortex activation", "Medial Prefrontal Cortex activity", "Medial prefrontal cortex function",
    "Motor cortex", "Nucleus Accumbens activity", "Orbitofrontal cortex function", "Parasympathetic system",
    "Pre-Supplementary Motor Area functional connectivity", "Prefrontal cortex volume and structure",
    "Prefrontal-limbic circuitry", "Resting State networks", "Reward and motivation circuits",
    "Right anterior insula network", "Salience network", "Somatosensory cortex", "Striatum connectivity",
    "Subcortical network (SCN)-ventral attention network (VAN)", "Substantia nigra", "Suprachiasmatic Nucleus",
    "Temporoparietal Junction", "Thalamocortical networks", "Thalamus volume", "Ventral striatum function",
    "Ventral Tegmental Area function", "Ventromedial prefrontal cortex function", "Visual processes",
    "Adenosine triphosphate", "Adrenocorticotropic Hormone", "Brain-derived neurotrophic factor",
    "Cholecystokinin", "Corticotropin-releasing hormone", "Cortisol", "Cytokines", "Dopamine", "Dopamine D1 receptor",
    "Estrogens", "Gamma-aminobutyric acid", "Glucocorticoids", "Glutamate", "Glutamate-Glutamine cycle",
    "Inflammatory molecules", "Interleukin 1β", "Interleukin 6", "Leptin", "Neuronal glutamate transporter EAAT3",
    "Neuropeptide S", "Neuropeptide Y", "Neurosteroids", "Norepinephrine", "Oxytocin", "Postsynaptic Density-95",
    "Serotonin", "Serotonin-1B receptor", "Synapsin-1", "Testosterone", "Thyroid hormone", "TNF-α", "Vasopressin",
    "α2-noradrenergic receptor"
]


def map_biomarker_terms(user_input):
    """
    Call the Groq API based on user input, mapping the input biomarkers to standardized Biomarker entries.
    """
    # 优化后的Prompt
    prompt = f"""
You are an expert in biological markers and neuroscience. Your task is to map the given input terms to standardized biomarker names.

The input is a list of biomarker-related terms. Compare each term with the standardized biomarker list below and return only the matched terms from the list:

{', '.join(biomarker_list)}

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
    user_input = "Cortisol"
    mapped_terms = map_biomarker_terms(user_input)
    print(f"Mapped Terms: {mapped_terms}")
