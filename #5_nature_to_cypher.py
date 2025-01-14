import os
import requests

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# API 配置
GROQ_API_ENDPOINT = os.getenv("GROQ_API_ENDPOINT")
API_KEY = os.getenv("GROQ_API_KEY")

# 提示模板
PROMPT_TEMPLATE = """
You are an AI assistant skilled in translating natural language questions into Neo4j Cypher queries. Below are the node and relationship definitions, followed by example mappings between natural language questions and Cypher queries.

### Node properties:
- RDoCStructure {id: STRING, name: STRING, rdoc_structure_level: STRING}
- RDoCElement {id: STRING, name: STRING, category: STRING}
- Disorder {id: STRING, name: STRING}
- Biomarker {id: STRING, name: STRING}
- BiomarkerCategory {id: STRING, name: STRING}
- Diagnosis {id: STRING, name: STRING}
- DiagnosisCategory {id: STRING, name: STRING}
- Measurement {id: STRING, name: STRING, target: STRING}
- MeasureCategory {id: STRING, name: STRING}
- RiskFactor {id: STRING, name: STRING}
- RiskCategory {id: STRING, name: STRING}
- Symptom {id: STRING, name: STRING}
- SymCategory {id: STRING, name: STRING}
- Treatment {id: STRING, name: STRING, category: STRING}
- TreatCategory {id: STRING, name: STRING}
- Class {id: STRING, name: STRING}

### Treatment categories:
"Dietary Supplements",
"Mind-Body Therapies",
"Mindfulness-Based Interventions",
"Other Therapy",
"Sensory Art Therapies",
"Antidepressants",
"Anxiolytics",
"Hormonal Drugs",
"Others",
"Convulsive Therapy",
"Cognitive Behavioral Therapy"

### Relationship properties:
- CONTAINS {description: STRING}
- HAS_ELEMENT {description: STRING}
- HAS_BIOMARKER {description: STRING}
- BELONGS_TO {description: STRING}
- HAS_DIAGNOSIS {description: STRING}
- HAS_MEASUREMENT {description: STRING}
- HAS_RISK {description: STRING}
- HAS_SYMPTOM {description: STRING}
- HAS_TREATMENT {description: STRING}
- HAS_COMORBIDITY {description: STRING}
- DIFFERENTIAL_DIAGNOSIS {description: STRING}
- CATEGORY {description: STRING}
- MAPPED_TO_RDOC {description: STRING}

### Example Mappings:
- Natural Language: "What are the symptoms of Major Depressive Disorder?"
  Cypher Query: "MATCH (disorder:Disorder {name: 'Major Depressive Disorder'})-[:HAS_SYMPTOM]->(sym:Symptom) RETURN sym.name"

- Natural Language: "What are the common symptoms of Generalized Anxiety Disorder?"
  Cypher Query: "MATCH (disorder:Disorder {name: 'Generalized Anxiety Disorder'})-[:HAS_SYMPTOM]->(sym:Symptom) RETURN sym.name"

- Natural Language: "Which diseases are associated with Insomnia?"
  Cypher Query: "MATCH (sym:Symptom {name: 'Insomnia'})<-[:HAS_SYMPTOM]-(disorder:Disorder) RETURN disorder.name"

- Natural Language: "Which disorders are linked to Stress?"
  Cypher Query: "MATCH (sym:Symptom {name: 'Stress'})<-[:HAS_SYMPTOM]-(disorder:Disorder) RETURN disorder.name"

- Natural Language: "What treatments are available for Anxiety Disorder?"
  Cypher Query: "MATCH (disorder:Disorder {name: 'Anxiety Disorder'})-[:HAS_TREATMENT]->(treat:Treatment) RETURN treat.name"

- Natural Language: "How is Bipolar Disorder diagnosed?"
  Cypher Query: "MATCH (disorder:Disorder {name: 'Bipolar Disorder'})-[:HAS_DIAGNOSIS]->(diagnosis:Diagnosis) RETURN diagnosis.name"

- Natural Language: "What biomarkers are linked to Schizophrenia?"
  Cypher Query: "MATCH (disorder:Disorder {name: 'Schizophrenia'})-[:HAS_BIOMARKER]->(b:Biomarker) RETURN b.name"

- Natural Language: "What are the biomarkers for Alzheimer's Disease?"
  Cypher Query: "MATCH (disorder:Disorder {name: 'Alzheimer\'s Disease'})-[:HAS_BIOMARKER]->(b:Biomarker) RETURN b.name"

- Natural Language: "What are the risk factors for PTSD?"
  Cypher Query: "MATCH (disorder:Disorder {name: 'PTSD'})-[:HAS_RISK]->(rf:RiskFactor) RETURN rf.name"

- Natural Language: "What risk factors contribute to Anxiety?"
  Cypher Query: "MATCH (disorder:Disorder {name: 'Anxiety'})-[:HAS_RISK]->(rf:RiskFactor) RETURN rf.name"

- Natural Language: "What measurements are used for OCD diagnosis?"
  Cypher Query: "MATCH (disorder:Disorder {name: 'OCD'})-[:HAS_MEASUREMENT]->(measure:Measurement)
  MATCH (measure)-[:MAPPED_TO_RDOC]->(re:RDoCElement)
  MATCH (re)<-[:HAS_ELEMENT]-(rdoc_structure:RDoCStructure)
  RETURN measure.name, rdoc_structure.name"

- Natural Language: "How can I detect if I have a PD"
  Cypher Query: "MATCH (disorder:Disorder {name: 'PD'})-[:HAS_MEASUREMENT]->(measure:Measurement)
  MATCH (measure)-[:MAPPED_TO_RDOC]->(re:RDoCElement)
  MATCH (re)<-[:HAS_ELEMENT]-(rdoc_structure:RDoCStructure)
  RETURN measure.name, rdoc_structure.name"

- Natural Language: "What other mental disorders may coexist with depression?"
  Cypher Query: "MATCH (disorder:Disorder {name: 'depression'})-[:HAS_COMORBIDITY]->(comorbidity:Disorder) RETURN comorbidity.name"

- Natural Language: "What other mental disorders need to be considered in the differential diagnosis of depression?"
  Cypher Query: "MATCH (disorder:Disorder {name: 'depression'})-[:DIFFERENTIAL_DIAGNOSIS]->(dd:Disorder) RETURN dd.name"

- Natural Language: "What antidepressants are commonly prescribed for Major Depressive Disorder?"
  Cypher Query: "MATCH (disorder:Disorder {name: 'Major Depressive Disorder'})-[:HAS_TREATMENT]->(treatment:Treatment) WHERE treatment.category = 'Antidepressants' RETURN treatment.name"

- Natural Language: "I've been experiencing insomnia lately, getting aggressive behavior easily, and not daring to make poor eye contact with others. What disease might I have?"
  Cypher Query: "MATCH (sym:Symptom)-[:HAS_SYMPTOM]-(disorder:Disorder) WHERE sym.name IN ['Insomnia', 'Aggressive behavior', 'Poor eye contact'] RETURN disorder.name, COUNT(sym) AS symptom_count ORDER BY symptom_count DESC"

### Task:
Translate the following natural language question into a valid Neo4j Cypher query:
"{user_query}"
Ensure the query adheres to the database schema provided above and only return the Cypher query.
"""

# 自然语言转 Cypher 查询
def natural_language_to_cypher(user_query):
    # Ensure that the user_query is correctly inserted into the prompt
    prompt = PROMPT_TEMPLATE.replace("{user_query}", user_query)
    
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are an expert in Cypher query generation."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 150
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    try:
        response = requests.post(GROQ_API_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        cypher_query = response.json()['choices'][0]['message']['content'].strip()
        return cypher_query
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except KeyError:
        print("Failed to extract Cypher query from the response.")
        return None

