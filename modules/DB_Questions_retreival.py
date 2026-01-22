import sqlite3
from google import genai
from dotenv import load_dotenv
import os

# --------- This function will be used to retreive the Questions/Answers from the Sqlite Database ----------

def Retreive_Questions(Subject):
    
# ------ Connecting to the Notes Database ------

    conn=sqlite3.connect("Notes.db")
    cursor=conn.cursor()

    Query=f"SELECT Notes_Title, Long_QA, Short_QA FROM {Subject} "
    cursor.execute(Query)
    all=cursor.fetchall()
    conn.close()

    
# ----------- Getting and Formatting the Q/A ------------
    
# ----- Separate lists for Short and Long Q/A -----

    Short = []
    Long = []
    Title=[]

# ----- Loop through each tuple using index numbers -----
    for i in range(len(all)):
        
        if all[i][0]:  
            Title.append(all[i][0])
        # First element = Short Q/A
        if all[i][1]:  
            Short.append(all[i][1])

        # Second element = Long Q/A
        if all[i][2]:  
            Long.append(all[i][2])

    formatted_output=Title + Short + Long

    return formatted_output

