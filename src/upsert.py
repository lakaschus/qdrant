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

collection_name = "personal_data"

# Connect to Qdrant
qdrant = QdrantClient(
    QDRANT_URL, 
    prefer_grpc=True,
    api_key=QDRANT_API_KEY,
)

with open("src/schema_config.json", "r") as f:
    schema = json.load(f)

# Create the collection
collections = qdrant.get_collections()
if collection_name in [coll[1][0].name for coll in list(collections)]:
    qdrant.delete_collection(collection_name)
        

qdrant.create_collection(collection_name, vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE))


# Load the data from the JSON file
with open("src/test_data.json", "r") as f:
    data = json.load(f)
    
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Insert the data into the collection
for i, payload in enumerate(data["experts"]):
    print(payload)
    vector = embeddings.embed_query(str(payload))
    qdrant.upsert(
    collection_name=f"{collection_name}",
    points=[
        models.PointStruct(
            id=i,
            vector=vector,
            payload=payload,
        )
    ]
)