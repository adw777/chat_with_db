from pymongo import MongoClient
from groq import Groq

# Initialize Groq client
client = Groq()

def natural_language_to_nosql(question):
    schema = """
    Collections:
    1. customers
       Fields: _id (int), name (string), country (string), email (string)

    2. software
       Fields: _id (int), name (string), version (string), release_date (string)

    3. sales
       Fields: _id (int), software_id (int), customer_id (int), sale_date (string), sale_amount (float), payment_method (string)
    """

    prompt = f"""
    Given the following MongoDB schema:

    {schema}

    Generate a MongoDB query to answer the following question:
    {question}

    Provide only the MongoDB query without any additional explanation. Use the PyMongo syntax.
    """

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-8b-instant",
        max_tokens=300,
        temperature=0.2,
    )

    nosql_query = response.choices[0].message.content.strip()
    
    return nosql_query

def execute_nosql_query(nosql_query):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['software_sales_database']
    
    # Execute the query
    # Assuming the nosql_query is a valid PyMongo query string
    try:
        # Evaluate the query safely
        result = eval(nosql_query)
        return list(result)
    except Exception as e:
        raise Exception(f"Error executing query: {e}")

def main():
    while True:
        user_query = input("Enter your question (or 'quit' to exit): ")
        if user_query.lower() == 'quit':
            break
        
        nosql_query = natural_language_to_nosql(user_query)
        print(f"Generated MongoDB Query: {nosql_query}")
        
        try:
            results = execute_nosql_query(nosql_query)
            print("Query Results:")
            for row in results:
                print(row)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
