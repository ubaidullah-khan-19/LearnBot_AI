import os
from pathlib import Path
import sqlite3

def Save_File(streamlit_File,subject,Title): #Saves the files and returns the loacation of the file

# ---------- Validating the Subject -----------

    if subject in ["Chemistry","Computer Science","English","Geography","History","Maths","Physics"]:

# ----------- Setting up the save Folder where the file will be Saved -----------

        save_folder = Path(__file__).parent.parent/f"Subjects/{subject}"
        os.makedirs(save_folder, exist_ok=True)

        uploaded_file=streamlit_File
        
        if uploaded_file is not None:
            save_path = save_folder / uploaded_file.name

# ---------- Saving the file to the save Folder ----------

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                return save_path
            
# --------- Saving Notes with their titles ----------

    conn=sqlite3.connect("Notes.db")
    cursor=conn.cursor()
    Query2=f"INSERT INTO {subject} (Notes_Title) VALUES (?)"
    cursor.execute(Query2,(Title,))
    conn.commit()
    conn.close()

# ---------- Saving the location of the File to Secure the Script from Future anamolies and for logical usage purposes -----------
# 
    #         conn=sqlite3.connect("Logic_helper_filenames.db")
    #         conn.execute(""""CREATE TABLE IF NOT EXISTS File_names(
    #              id INTEGER PRIMARY KEY,
    #              Embedded_Files STRING)
    #              """)
    #         cursor=conn.cursor()
    #         cursor.execute("INSERT INTO File_names(Embedded_Files) VALUES(?)",(save_path,))
    #         return save_path
    #     else:
    #         st.error("No File Uploaded!")

    # else:
    #     st.error("Invalid Subject!")

    