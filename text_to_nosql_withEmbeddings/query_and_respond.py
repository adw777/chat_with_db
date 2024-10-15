import os
import json  
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

model = SentenceTransformer('all-MiniLM-L6-v2')

groq_client = Groq(api_key=GROQ_API_KEY)

def query_and_respond(user_query):
    # Create embedding for the user query
    query_embedding = model.encode(user_query).tolist()
    
    # Perform vector search in Qdrant
    search_results = qdrant_client.search(
        collection_name="document_embeddings",
        query_vector=query_embedding,
        limit=3  # Adjust this number based on how many relevant documents you want to consider
    )
    
    # Extract the relevant documents from the search results
    relevant_docs = [result.payload["full_document"] for result in search_results]
    
    prompt = f"""Based on the following documents:

{json.dumps(relevant_docs, indent=2)}

Please answer the following question:
{user_query}

Provide a concise and informative response."""

    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful data analysis assistant that provides accurate and concise information based on the given data."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
     while True: 
        user_query = input("Enter your question (or type 'exit' to quit): ")
        if user_query.lower() == 'exit': 
            print("Exiting the program.")
            break
        response = query_and_respond(user_query)
        print("\nResponse:")
        print(response)
