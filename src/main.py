from qdrant_client import QdrantClient
from qdrant_client.http import models
import json
# Load QDRANT_API_KEY from environment
from dotenv import load_dotenv
import os
load_dotenv()
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
doc_store = Qdrant.from_texts(
    texts, embeddings, url="<qdrant-url>", api_key="<qdrant-api-key>", collection_name="texts"
)

# Connect to Qdrant
qdrant = QdrantClient(
    "https://78d0f8ed-dfb6-437b-ae44-688aedf1c4ce.us-east-1-0.aws.cloud.qdrant.io", 
    prefer_grpc=True,
    api_key=QDRANT_API_KEY,
)

with open("src/schema_config.json", "r") as f:
    schema = json.load(f)

# Create the collection
collection_name = "personal_data"
collections = qdrant.get_collections()
if collection_name in [coll[1][0].name for coll in list(collections)]:
    qdrant.delete_collection(collection_name)
        

qdrant.create_collection(collection_name, vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE))


# Load the data from the JSON file
with open("src/test_data.json", "r") as f:
    data = json.load(f)

# Insert the data into the collection
for expert in data["experts"]:
    qdrant.upsert(
    collection_name=f"{collection_name}",
    points=[
        models.PointStruct(
            id=1,
            vector=[0.05, 0.61, 0.76, 0.74],
            payload={
                "city": "Berlin", 
                "price": 1.99,
            },
        )
    ]
)