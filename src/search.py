from qdrant_client import QdrantClient
from qdrant_client.http import models
import json
# Load QDRANT_API_KEY from environment
from dotenv import load_dotenv
import os
load_dotenv()
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings

COLLECTION_NAME = "personal_data"

# Connect to Qdrant
qdrant = QdrantClient(
    QDRANT_URL, 
    prefer_grpc=True,
    api_key=QDRANT_API_KEY,
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def query(string):
    results = qdrant.search(COLLECTION_NAME, query_vector=embeddings.embed_query(string))
    return results[0].payload['first_name']

if __name__ == "__main__":
    queries_1 = ["Python", "Programming", "Developing tools", "Application", "Software", "Artificial intelligence", "He is developing some code to help humanity"]
    queries_2 = ["Beethoven", "Mozart", "Classical Music", "Piano", "Symphony", "Concert", "He is a great composer"]
    print("This should match with the first expert Phillip")
    for string in queries_1:
        print(query(string))
    
    print("\nThis should match with the second expert Yao")
    for string in queries_2:
        print(query(string))