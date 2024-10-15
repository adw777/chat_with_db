from pymongo import MongoClient
from groq import Groq
from text_to_Nosql import natural_language_to_nosql, execute_nosql_query

# Initialize Groq client
client = Groq()

def get_schema():
    return """
    Collections:
    1. customers
       Fields: _id (int), name (string), country (string), email (string)

    2. software
       Fields: _id (int), name (string), version (string), release_date (string)

    3. sales
       Fields: _id (int), software_id (int), customer_id (int), sale_date (string), sale_amount (float), payment_method (string)
    """

def generate_insight(user_query, nosql_query, query_results):
    schema = get_schema()
    
    prompt = f"""
    Context:
    User Query: {user_query}
    MongoDB Query Code:
    {nosql_query}
    Query Results (first 5): {query_results[:5]}
    Total Results: {len(query_results)}
    {schema}

    Task: Analyze the query results and provide an insight to the user's original question using the data from the query result.  
    Keep the response concise and short. Do not add any data on your own!

    Insight:
    """

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-8b-instant",
        max_tokens=200,
        temperature=0.5,
    )

    return response.choices[0].message.content

def main():
    while True:
        user_query = input("Enter your question (or 'quit' to exit): ")
        if user_query.lower() == 'quit':
            break
        
        nosql_query = natural_language_to_nosql(user_query)
        print(f"Generated MongoDB Query Code:")
        print(nosql_query)
        
        try:
            results = execute_nosql_query(nosql_query)
            print("\nQuery Results (first 5):")
            for row in results[:5]:
                print(row)
            print(f"\nTotal results: {len(results)}")
            
            insight = generate_insight(user_query, nosql_query, results)
            print("\nInsight:")
            print(insight)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()