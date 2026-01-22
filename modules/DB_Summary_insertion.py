from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from google import genai
from dotenv import load_dotenv
import os
import sqlite3

def Summarize(File_Location,Subject):

# ---------- Getting Text into a Cleaner and Non PDF text form ----------

    if Subject in ["Chemistry","Computer Science","English","Geography","History","Maths","Physics"]:
        loader=PyPDFLoader(file_path=File_Location)
        docs=loader.load()
        clean_text = "\n\n".join([doc.page_content.strip() for doc in docs])

# ---------- Setting up the LLM ----------

        load_dotenv()
        API=os.getenv("API_Key")
        client=genai.Client(api_key=API)

# ---------- LLM for Detailed Summary ----------

        response=client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f'''You are an AI whose only purpose is summarization. 
Summarize the TEXT into approximately 1/5th of its original length.
TEXT : {clean_text}
Rules:
- Produce a well-thought, logically structured, high-quality summary.
- Keep only the essential ideas, key arguments, and important facts.
- No unnecessary wording, no filler sentences, no repetition.
- Do not ask questions or request clarification. Summarize in one go.
- Do NOT add any external information not found in the text.
- The output must be precise, clear, and sharply to the point.

'''
        )
        Detailed_Summary=response.text
    

# ---------- LLM for Brief Summary ----------

        response2=client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f'''You are an AI whose only purpose is to capture the core essence of a text. 
Summarize the TEXT into approximately 1/8th of its original length.
TEXT : {clean_text}
Your summary must:
- Focus on the deepest meaning, key insights, and essential ideas.
- Preserve the reasoning, message, and intent of the original text.
- Avoid listing, outlining, or restating every section.
- Avoid shallow paraphrasing.
- Do not include minor details, examples, or side points.
- Produce a well-written, coherent, natural summary that reads like an expert distilled the text.
- Do not ask questions or seek clarification. Summarize in one go.
- Do not add any outside information.



'''
        )
        Brief_Summary=response2.text
    



# ---------- Saving the Summaries to the Database -----------

        if Detailed_Summary and Brief_Summary:
            conn=sqlite3.connect("Notes.db")
            cursor=conn.cursor()
            query = f"INSERT INTO {Subject} (Detailed_Summary, Brief_Summary) VALUES (?, ?)"
            cursor.execute(query, (Detailed_Summary, Brief_Summary))
            conn.commit()
            conn.close()

    
    