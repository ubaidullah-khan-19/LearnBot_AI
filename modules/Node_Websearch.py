from ddgs import DDGS
from google import genai
from dotenv import load_dotenv
import json
import os


def web_search(Query):
    load_dotenv()
    api=os.getenv("API_Key")
    try:
        ddgs=DDGS()
        results=list(ddgs.text(Query,max_results=5))
        if results:
            client = genai.Client(api_key=api)  
            response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents=(f'''
Summarize the following search results to answer this question: "{Query}"

Search Results: {results}

Provide a clear, factual summary focusing on:
1. Key facts and numbers
2. Latest information
3. Relevant sources
'''))
            return response.text
        else:
            return "No results found"
    except Exception as e:
        return f"No results found due to {e} error"
        
    
    