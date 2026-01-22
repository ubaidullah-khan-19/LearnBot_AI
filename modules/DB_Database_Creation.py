import sqlite3

def Create_Database():

    conn=sqlite3.connect("Notes.db")
    cursor=conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS History(
               id INTEGER PRIMARY KEY,
               Notes_Title STRING,
               Brief_Summary TEXT,
               Detailed_Summary TEXT,
               Long_QA TEXT,
               Short_QA TEXT,
               Quiz TEXT)
                   ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Geography(
                   id INTEGER PRIMARY KEY,
                   Notes_Title STRING,
                   Brief_Summary TEXT,
                    Detailed_Summary TEXT,
                    Long_QA TEXT,
                    Short_QA TEXT,
                    Quiz TEXT)
                   ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Chemistry(
                    id INTEGER PRIMARY KEY,
                    Notes_Title STRING,
                    Brief_Summary TEXT,
                    Detailed_Summary TEXT,
                    Long_QA TEXT,
                    Short_QA TEXT,
                    Quiz TEXT)
                   ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Computer_Science(
                    id INTEGER PRIMARY KEY,
                    Notes_Title STRING,
                    Brief_Summary TEXT,
                    Detailed_Summary TEXT,
                    Long_QA TEXT,
                    Short_QA TEXT,
                    Quiz TEXT)
                   ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS English(
                    id INTEGER PRIMARY KEY,
                    Notes_Title STRING,
                    Brief_Summary TEXT,
                    Detailed_Summary TEXT,
                    Long_QA TEXT,
                    Short_QA TEXT,
                    Quiz TEXT)
                   ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Maths(
                    id INTEGER PRIMARY KEY,
                    Notes_Title STRING,
                    Brief_Summary TEXT,
                    Detailed_Summary TEXT,
                    Long_QA TEXT,
                    Short_QA TEXT,
                    Quiz TEXT)
                   ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Physics(
                    id INTEGER PRIMARY KEY,
                    Notes_Title STRING,
                    Brief_Summary TEXT,
                    Detailed_Summary TEXT,
                    Long_QA TEXT,
                    Short_QA TEXT,
                    Quiz TEXT)
                   ''')

Create_Database()



    
