# -------------------- IMPORTING ALL THE REQUIRED MODULES AND LIBRARIES --------------------

from google import genai
from typing import TypedDict,Annotated,Literal
from google import genai
from langgraph.graph import StateGraph,START,END
from modules import Node_Calculator, Node_RAG, Node_Research_Agent, Node_Websearch
from modules import DB_Database_Creation,DB_Questions_Insertion,DB_Questions_Insertion,DB_Questions_retreival, DB_Summary_insertion, DB_Summary_Retreival, DB_Vector_Embedding, LOCAL_File_saving
import streamlit as st
from dotenv import load_dotenv
import time
import os

# ---------- Configuring API Keys and LLM clients ----------

load_dotenv()
api= os.getenv("API_Key")
client=genai.Client(api_key=api)

# ---------- Creating a Class "Save_file" to group all functions related to file saving ----------

class Save_file():

    @staticmethod
    def Saving_Locally(saved_path,subject): # To save summary and Q/A of the file to sqlite database
        DB_Questions_Insertion.Make_Save_Questions(saved_path, subject) # To make Q/A of the file using LLM and saving it
        DB_Summary_insertion.Summarize(saved_path, subject) # To make Summary of the file using LLM and saving it
        return True
    @staticmethod
    def tSaving_Vecor(saved_path): # To save the File in Vector Database Qdrant
        DB_Vector_Embedding.File_Embed(saved_path) # Makes Chunks of File contents and save them to Vector Database Qdrant
        return True
    @staticmethod
    def Saving_all(saved_path, subject): # Combines both Vector and Sqlite database functions above and save the file
        DB_Questions_Insertion.Make_Save_Questions(saved_path, subject)
        DB_Summary_insertion.Summarize(saved_path, subject)
        DB_Vector_Embedding.File_Embed(saved_path)
        return True

class State(TypedDict):
     do_websearch: bool
     do_research: bool
     do_calculate: bool
     do_semantic_search: bool
     Agent: bool
     semantic_search_result: str
     Web_search_result: str
     Calculate_result: str
     Research_Result: str
     user_Query: str
     Final_Answer: str

def Semantic_search(state: State):
     User_Query=state["user_Query"]
     status = st.empty()  
     status.subheader("Doing Semantic Search...")
     Semantic_search_result=Node_RAG.Semantic_Search(User_Query)
     status.empty() 

     if Semantic_search_result:
          state["semantic_search_result"] = Semantic_search_result
          status.success("Semantically searched from Notes Successfully")
          time.sleep(2)
          status.empty()
          return state
     
def Calculate(state: State):
     Query=state["user_Query"]
     status = st.empty()  
     status.subheader("Solving and Calculating...")
     Calculation=Node_Calculator.Calculate(Query=Query)
     status.empty() 
          
     if Calculation:
          state["Calculate_result"]=Calculation
          status.success("Solved Successfully!")
          time.sleep(2)
          status.empty()
          return state

def Web_search(state: State):
     Query=state["user_Query"]
     status = st.empty()  
     status.subheader("Searching the Web...")
     Search_Result=Node_Websearch.web_search(Query=Query)
     status.empty()

     if Search_Result:
          state["Web_search_result"]=Search_Result
          status.success("Web Searched Successfully!")
          time.sleep(2)
          status.empty()
          return state

def Research(state: State):
     Query=state["user_Query"]
     status = st.empty()  
     status.subheader("Researching the Topic...")
     Deep_Searched=Node_Research_Agent.Research(Query=Query)
     status.empty()

     if Deep_Searched:
          state["Research_Result"]=Deep_Searched
          status.success("Topic Deeply Researched Successfully!")
          time.sleep(2)
          status.empty()
          return state
     
def Agent(state: State):
     Query=state["user_Query"]

     if "History" not in st.session_state:
          st.session_state.history=[]

     if Query:
          st.session_state.history.append(Query)
          Memory = "\n".join(x for x in st.session_state.history if x)
     
          Web_search=state["Web_search_result"]
          Researched=state["Research_Result"]
          Calculated=state["Calculate_result"]
          Semantic_searched=state["semantic_search_result"]

# ----------------------------------------------------------------------------

          if state["do_websearch"]==True:
               prompt=f'''
You are the Web Search Answer Agent.

You receive:
- User Query: "{Query}"
- Node Output (web search findings): "{Web_search}"
- Memory (previous user messages): "{Memory}"

Rules:
1. Web search output is authoritative. DO NOT modify it.
2. You may reorganize, format, or clarify, but never change the meaning.
3. Quote the web search output clearly when using it.
4. Use memory ONLY for conversational flow (tone, continuity). 
   Never assume you performed the web search yourself.
5. Do not question or comment on how you received the web results.
6. If web results do not answer fully, state politely: 
   "The provided search results do not fully answer this question."

Produce a polished, structured answer using:
- paragraphs
- bullet points
- short explanations

Now respond to the user. '''
          
               response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
               )
               responses=response.text
               if responses:
                    state["Final_Answer"]=responses
                    return state
     
# ---------------------------------------------------------

          elif state["do_calculate"]==True:
               prompt=f'''
You are the Calculator Explanation Agent.

You receive:
- User Query: "{Query}"
- Node Output (calculation result): "{Calculated}"
- Memory: "{Memory}"

Rules:
1. The calculation result is final. DO NOT change numbers.
2. You may explain how the result answers the question, but do not recalc.
3. Quote the numeric result exactly.
4. Use memory only for conversational continuity.
5. If the calculation does not fully solve the question, state:
   "The computation result does not fully answer the question."

Provide a concise, clear mathematical explanation.

Now respond to the user.
'''
               response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
               )
               responses=response.text
               if responses:
                    state["Final_Answer"]=responses
          
# --------------------------------------------------------------------

          elif state["do_research"]==True:
               prompt=f'''
You are the Research Explanation Agent.

You receive:
- User Query: "{Query}"
- Node Output (research findings): "{Researched}"
- Memory (previous user queries): "{Memory}"

Rules:
1. Treat the node output as the final research result. Do NOT alter it.
2. You may add short clarifications or explanations for better understanding.
3. Quote the research output when referencing it.
4. Use memory ONLY for conversational flow, not for new facts.
5. Never imply you performed the research; simply use the provided output.
6. If the research output does not fully answer the question, state:
   "The provided research content does not cover the full answer."

Produce a refined, structured, human-friendly explanation.

Now respond to the user.

'''
               response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
               )
               responses=response.text
               if responses:
                    state["Final_Answer"]=responses
                    return state
          
# -------------------------------------------------------------------------

          elif state["Agent"]==True:
               prompt=f'''
You are the General Tutor Agent.

You receive only:
- User Query: "{Query}"
- Memory (previous user messages): "{Memory}"

Rules:
1. Provide a clear, structured, high-quality explanation to the User Query.
2. Use memory ONLY for conversational flow, tone, and personalization.
   Never invent facts based on memory.
3. Do NOT mention nodes, tools, or any missing outputs.
4. Do NOT say anything like “I didn’t get data” or “I cannot see node output”.
   You should simply answer confidently based on your own understanding.
5. Keep the tone professional, friendly, and helpful.
6. If the question is unclear, ask for clarification politely.

Deliver a polished, complete answer that feels human and fluent.

Now respond to the user.

'''
               response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
               )
               responses=response.text
               if responses:
                    state["Final_Answer"]=responses
                    return state

# ----------------------------------------------------------------------------

          elif state["do_semantic_search"]==True:
               prompt=f'''
You are the Notes Retrieval (RAG) Answer Agent.

You receive:
- User Query: "{Query}"
- Node Output (semantic search retrieved notes): "{Semantic_searched}"
- Memory: "{Memory}"

Rules:
1. The notes retrieved are authoritative; DO NOT change their meaning.
2. You may rephrase for clarity but never alter facts.
3. Quote note fragments exactly when referencing them.
4. Use memory only for casual flow, NEVER to add new facts.
5. Do not question why these notes were retrieved.
6. If the notes do not contain enough information, say:
   "The retrieved notes do not have enough information for a full answer."


Present the answer cleanly, structured, and easy to read.

Now respond to the user.

'''
               response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
               )
               responses=response.text
               if responses:
                    status=st.empty()
                    status.subheader("Finalizing and Enhancing the Semantic Search result")
                    state["Final_Answer"]=responses
                    status.empty()
                    return state

# ----------------------------------------------------------------------------

def router(state: State):
     Query=state["user_Query"]
     
     prompt=f'''
You are a smart query router AI. I will give you a User Question. 
Your task is to determine which processing node should handle it. 

Nodes available:

1. "Calculate" → for any question requiring calculations, math operations, or numeric reasoning.
2. "Semantic" → for questions answerable from existing notes when user explicitly mention his/her notes or knowledge already embedded in our vector store.
3. "Research" → for questions that require detailed investigation, summarization, or reasoning using multiple sources.
4. "Web" → for questions that require up-to-date, real-time information from the internet (news, stock prices, weather, events, etc.)
5. "Agent" → default node. Use this if the question does not clearly require any of the other nodes.

Rules:

- Analyze the user's question carefully.
- Respond with **ONLY one node name exactly as listed**: "Calculate", "Semantic", "Research", "Agent" or "Web".
- Do NOT add any explanation, punctuation, or extra text. Just the node name.
- Make the decision based on the question content alone.

User Question: "{Query}" '''
     
     response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
     decision=str(response.text).strip().upper()

     if decision=="AGENT":
          state["do_calculate"] = False
          state["do_research"] = False
          state["do_websearch"] = False
          state["do_semantic_search"] = False
          state["Agent"]=True
          
     elif decision=="SEMANTIC":
          state["do_calculate"] = False
          state["do_research"] = False
          state["do_websearch"] = False
          state["do_semantic_search"] = True
          state["Agent"]=False

     elif decision=="WEB":
          state["do_calculate"] = False
          state["do_research"] = False
          state["do_websearch"] = True
          state["do_semantic_search"] = False
          state["Agent"]=False

     elif decision=="CALCULATE":
          state["do_calculate"] = True
          state["do_research"] = False
          state["do_websearch"] = False
          state["do_semantic_search"] = False
          state["Agent"]=False

     elif decision=="RESEARCH":
          state["do_calculate"] = False
          state["do_research"] = True
          state["do_websearch"] = False
          state["do_semantic_search"] = False
          state["Agent"]=False

     return state

def Classifier(state: State):
    
    if state["do_calculate"]:
        return "CALCULATE"
    
    elif state["Agent"]:
        return "AGENT"
    
    elif state["do_research"]:
        return "RESEARCH"
    
    elif state["do_semantic_search"]:
        return "SEMANTIC"
    
    elif state["do_websearch"]:
        return "WEB"
    
# ---------- Creating GUI ---------

st.title("LearnBot AI")

with st.sidebar:
     st.header("Modes")
     Mode = st.radio(
     "Choose Mode",
     [":rainbow[AI Tutor]", "Summaries", "Questions/Answers","Upload"],
     captions=[
         "Your Personal AI learning Tutor",
         "Summaries of your notes",
         "Q/A from your notes",
         "Upload new files to notes"
     ])
     
# ---------- Defining and Configuring the main AI Agent -----------

if Mode==":rainbow[AI Tutor]":
     
     st.header("Your Personal AI learning Tutor")
     Query=st.chat_input("Ask anything academic")
     Graph=StateGraph(State)
     
     Graph.add_node("Agent",Agent)
     Graph.add_node("Web_search",Web_search)
     Graph.add_node("Semantic_search",Semantic_search)
     Graph.add_node("Research",Research)
     Graph.add_node("Calculate",Calculate)
     Graph.add_node("router", router) 

     Graph.set_entry_point("router")

     Graph.add_conditional_edges("router",Classifier,{"WEB": "Web_search", "CALCULATE": "Calculate","SEMANTIC": "Semantic_search","RESEARCH": "Research","AGENT": "Agent",})

     Graph.add_edge("Web_search", "Agent")
     Graph.add_edge("Semantic_search", "Agent")
     Graph.add_edge("Research", "Agent")
     Graph.add_edge("Calculate", "Agent")
     Graph.add_edge("Agent", END)

     if Query:

          initial_state: State={
          "do_websearch": False,
          "do_research": False,
          "do_calculate": False,
          "do_semantic_search": False,
          "Agent": True,
          "semantic_search_result": "",
          "Web_search_result": "",
          "Calculate_result": "",
          "Research_Result": "",
          "user_Query": Query,
           "Final_Answer": "" }

          Workflow=Graph.compile()

          Result=Workflow.invoke(initial_state)
          st.chat_message("user").write(Query)
          st.chat_message("assistant").write(Result["Final_Answer"])

# ---------- Defining the Summaries Retreiver Capability by calling Summary retreiver Module ----------

elif Mode=="Summaries":
    st.header("All Summaries of Your Notes")
    with st.form("Get Summaries"):
        Subject = st.radio(
     "Choose Subject:",
     ["Chemistry","Computer Science","English","Geography","History","Maths","Physics"])
        submit=st.form_submit_button("Fetch All Summaries",use_container_width=True)
    if Subject and submit:
         Summaries=DB_Summary_Retreival.Retreive_Summary(Subject)
         for i in Summaries:
              st.write(i)

# ---------- Defining the Q/A Retreiver Capability by calling Questions/Answers retreiver Module ----------

elif Mode=="Questions/Answers":
     st.header("All Questions/Answers of Your Notes")
     with st.form("Get Questions/Answers"):
        Subject = st.radio(
     "Choose Subject:",
     ["Chemistry","Computer Science","English","Geography","History","Maths","Physics"])
        submit=st.form_submit_button("Fetch All Questions/Answers",use_container_width=True)
     if submit:
          qsas=DB_Questions_retreival.Retreive_Questions(Subject)
          for i in qsas:
               st.write(i)
     
# ---------- Writing the Code For the Upload Capability by Calling the Summary insertion, File Saving and Q/A insertion Modules ---------

elif Mode=="Upload":
     
     with st.form("Upload Notes"):

        subject = st.selectbox("Choose Subject:", ["Chemistry","Computer Science","English","Geography","History","Maths","Physics"])
        file = st.file_uploader("Upload File", type=["pdf"])
        title=st.text_input("Enter Title of Notes")
        save_place = st.selectbox("Choose Database:", ["Save File Locally","Save in Vector Database","Save in Both"])
        Save=st.form_submit_button("Save Notes")

     if file and Save and title:
          saved_path = LOCAL_File_saving.Save_File(file, subject,Title=title) # saves the file locally and returns its file_location as saved_path

          if save_place=="Save File Locally":
               st.subheader("This could take some time")
               st.subheader("Wait...")
               saved=Save_file.Saving_Locally(saved_path,subject)
               st.success("File Uploaded Successfully")

          elif save_place=="Save in Vector Database":
               st.subheader("This could take some time")
               st.subheader("Wait...")
               saved=Save_file.Saving_Vector(saved_path) # calling Saving_Vector function from Save_File Class
               if saved:
                    st.success("File Uploaded Successfully")

          elif save_place=="Save in Both":
               st.subheader("This could take some time")
               st.subheader("Wait...")
               saved=Save_file.Saving_all(saved_path,subject)# calling Saving_all function from Save_File Class
               if saved:
                    st.success("File Uploaded Successfully")
            
     if Save and not file:
          st.error("Please Upload a File First!")
     
     if Save and not title:
          st.error("Please Give a Title First!")

          
     

     


     



