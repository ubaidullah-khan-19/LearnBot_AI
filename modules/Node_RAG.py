from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models
from google import genai
from dotenv import load_dotenv
import os

def Semantic_Search(Query):

    load_dotenv()
    API=os.getenv("API_Key")
    Qdrant_Server=os.getenv("http://localhost:6333")
    
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    client = QdrantClient(url=Qdrant_Server)
    vector_store=QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="MY_NOTES",
    embedding=embedding_model
    )

    relevant_result=vector_store.similarity_search(query=Query)
    response="\n\n\n".join([f"Page Content: {result.page_content}\n Page number: {result.metadata['page_label']}\n File location: {result.metadata['source']}"for result in relevant_result])
    return response