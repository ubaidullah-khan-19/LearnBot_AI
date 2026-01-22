import sqlite3
from google import genai
from dotenv import load_dotenv
import os

# ---------- This function will be used to retreive the summaries from the Sqlite database ----------

def Retreive_Summary(Subject):
    
# ------ Connecting tothe Sqlite Database ------    

    conn=sqlite3.connect("Notes.db")
    cursor=conn.cursor()

    Query=f"SELECT Brief_Summary, Detailed_Summary FROM {Subject}"
    cursor.execute(Query)
    all=cursor.fetchall()
    conn.close()

# ----------- Getting and Formatting the Summaries ------------
    
# ----- Separate lists for brief and detailed summaries -----

    Briefs = []
    Detailed = []

# ----- Loop through each tuple using index numbers -----
    for i in range(len(all)):
        
        # First element = Brief_Summary
        if all[i][0]:  # skip None or empty
            Briefs.append(all[i][0])

        # Second element = Detailed_Summary
        if all[i][1]:  # skip None or empty
            Detailed.append(all[i][1])

    formatted_output=Briefs + Detailed

    return formatted_output
        