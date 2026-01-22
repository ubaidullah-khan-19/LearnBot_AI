from pathlib import Path
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models
from langchain_huggingface import HuggingFaceEmbeddings
import sqlite3
import glob
import os
from dotenv import load_dotenv



def File_Embed(file_location): #  The location returned by save_file function

# ----- To avoid already embedded files to store in vector base again -----

#     conn=sqlite3.connect("Logic_helper_filenames.db")
#     cursor=conn.cursor()
#     cursor.execute("SELECT Embedded_Files FROM File_names")
#     Raw_File_names=cursor.fetchall()
#     Already_Embedded_files=[]
#     for i in Raw_File_names:
#         files=Raw_File_names[0]
#         Already_Embedded_files.append(files)

# ----- Extracting Text From PDF File -----

#     if file_location not in Already_Embedded_files:
        loader=PyPDFLoader(file_path=file_location)
        docs=loader.load()
    

# ----- Chunking -----

        splitter=RecursiveCharacterTextSplitter(
        chunk_size=120,
        chunk_overlap=40
        )
        Chunk=splitter.split_documents(documents=docs)

# ----- Configuring Embedding model -----

        embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        load_dotenv()
        URL=os.getenv("Qdrant_url")

# ----- Storing Data in Vector Store ------

        client=QdrantClient(url=URL)
        vector_store=QdrantVectorStore.from_documents(
        documents=Chunk,
        embedding=embedding_model,
        collection_name="MY_NOTES",
        distance="Cosine"
        )
    
        

    
