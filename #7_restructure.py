import requests
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# Groq API 端点和密钥
groq_api_endpoint = os.getenv("GROQ_API_ENDPOINT")
api_key = os.getenv("GROQ_API_KEY")
model_name = "llama3-70b-8192"

# 构建新的 enhanced_prompt
def build_enhanced_prompt(user_input, query_results):
    """
    Create a new prompt that includes the user's original question and the retrieval results in Neo4j.
    """
    results_str = ", ".join(
        record[key] 
        for record in query_results 
        for key in record.keys() 
        if key.endswith(".name")
    )
    
    enhanced_prompt = f"""
    You are an AI assistant specializing in professional knowledge retrieval. 
    Your task is to answer the user's question based strictly on the provided Neo4j database query results.

    **User Question:** {user_input}

    **Neo4j Query Results:** {results_str}

    **Instructions for Your Answer:**  
    1. Use the database query results as the foundation for your answer.  
    2. Provide a clear, structured response. Break the information into relevant sections by using bullet points and short paragraphs to organize the information effectively.  
    3. Explain how the results are relevant to the user's question, clarifying the connection between the keywords in the question and the database results in those short paragraphs.  
    4. Focus solely on the provided query results. Do not introduce information that is not directly related to the results or discuss similar or related concepts outside of what was retrieved.  
    5. If the results partially answer the question, indicate what the results reveal and explain any limitations without making assumptions or guesses.

    Now, provide your answer based on the above context.
    """
    return enhanced_prompt

# 调用 Groq API 并获取 LLM 输出
def invoke_llm(prompt):
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": model_name,
        "temperature": 0.7
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        response = requests.post(groq_api_endpoint, json=payload, headers=headers)
        response.raise_for_status()
        response_json = response.json()

        if 'choices' in response_json:
            llm_response = response_json['choices'][0]['message']['content']
            return llm_response
        else:
            return "No response from LLM."

    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM API: {e}")
        return "Error during LLM invocation."
