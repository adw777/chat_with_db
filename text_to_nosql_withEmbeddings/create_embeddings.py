import os
from dotenv import load_dotenv
from pymongo import MongoClient
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer
from bson import json_util
import json

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Qdrant connection
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

# Connect to Qdrant
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create a new collection in Qdrant
collection_name = "document_embeddings"
qdrant_client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=model.get_sentence_embedding_dimension(), distance=Distance.COSINE),
)

# function to convert MongoDB document to JSON-serializable format
def convert_mongo_doc_to_json(doc):
    return json.loads(json_util.dumps(doc))

# Fetch documents from MongoDB and create embeddings
documents = collection.find()
for idx, doc in enumerate(documents):
    # Convert the entire document to a JSON-serializable format
    doc_json = convert_mongo_doc_to_json(doc)
    
    # Create a text representation of the entire document for embedding
    text = json.dumps(doc_json, ensure_ascii=False)
    embedding = model.encode(text).tolist()
    
    # Store the embedding and the entire document in Qdrant
    qdrant_client.upsert(
        collection_name=collection_name,
        points=[
            {
                "id": idx,
                "vector": embedding,
                "payload": {
                    "full_document": doc_json,
                    "mongo_id": str(doc["_id"])
                }
            }
        ]
    )
    
    if idx % 100 == 0:
        print(f"Processed {idx} documents")

print("Embedding creation and storage complete!")
