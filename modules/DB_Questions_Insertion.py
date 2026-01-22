from pathlib import Path
import sqlite3
from langchain_community.document_loaders import PyPDFLoader
from google import genai
from dotenv import load_dotenv
import os

def Make_Save_Questions(File_Location,Subject):

# ---------- Getting Text into a Cleaner and Non PDF text form ----------

    loader=PyPDFLoader(file_path=File_Location)
    docs=loader.load()
    clean_text = "\n\n".join([doc.page_content.strip() for doc in docs])
    load_dotenv()

# ----------- Setting up LLMs ------------

    API=os.getenv("API_Key")
    client=genai.Client(api_key=API)

# ---------- LLM for Long Questions ----------
#   
    response=client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f'''You are an AI designed for one task only: 
Generate detailed, descriptive, exam-style LONG questions and their corresponding LONG answers from the TEXT.
TEXT : {clean_text}
Rules:
- Only generate questions and answers strictly based on the provided text.
- Each question must require explanation, understanding, or analysis.
- Answers must be complete, well-structured, and cover all important points.
- Do not add information that is not present in the user's text.
- Maintain high clarity and educational quality.
- Number the questions.

Output Format:
Q1: <Long Question>
A1: <Long, descriptive answer>

Q2: <Long Question>
A2: <Long, descriptive answer>'''
        )
    Questions=response.text

# --------- Setting up the Database -----------

    conn=sqlite3.connect("Notes.db")
    cursor=conn.cursor()

# ---------- Adding LONG Q/A to Database ----------

    query = f"INSERT INTO {Subject} (Long_QA) VALUES (?)"
    cursor.execute(query, (Questions,))
    conn.commit()

# ----------- LLM for SHORT Q/A -----------

    response2=client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f'''You are an AI designed for one task only:
Generate SHORT, clear, concept-checking questions and SHORT answers from the TEXT.
TEXT : {clean_text}
Rules:
- Only use information from the provided text.
- Keep both questions and answers simple, direct, and to the point.
- No unnecessary explanation.
- Do not invent any information.
- Questions should test definitions, terms, rules, or key ideas.
- Number the questions.

Output Format:
Q1: <Short Question>
A1: <Short Answer>

Q2: <Short Question>
A2: <Short Answer>'''
        )
    Shorts=response2.text

# ---------- Adding Short Q/A to Database ---------

    Query2=f"INSERT INTO {Subject} (Short_QA) VALUES (?)"
    cursor.execute(Query2,(Shorts,))
    conn.commit()
    conn.close()




