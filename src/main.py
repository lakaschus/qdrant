from qdrant_client import QdrantClient
import json

# Create a new qdrant client
client = QdrantClient("http://localhost:6333")

# Load the index_config from index_config.json
index_config = json.load(open("index_config.json"))
client.create_collection("personal_data", index_config)

# Function to create a new vector database index
def create_index(collection_name, dimension):
    index_config = {
        "force_create": True,
        "index_type": "Flat",
        "metric_type": "L2",
        "dimension": dimension
    }
    client.create_collection(collection_name, index_config)

# Function to read/search data
def search(collection_name, query, top_k=10):
    search_result = client.search(collection_name, query, top_k=top_k)
    return search_result

# Function to create new data
def create_data(collection_name, data, ids):
    client.upsert(collection_name, data, ids)

# Function to delete data
def delete_data(collection_name, ids):
    client.delete(collection_name, ids)