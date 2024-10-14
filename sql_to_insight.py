import sqlite3
from text_to_sql2 import natural_language_to_sql, execute_sql_query
from groq import Groq

# Initialize Groq client
client = Groq()

def get_table_schema():
    return """
    Table: sales
    Columns:
    - Sale_ID (int, primary key)
    - Software_Name (text)
    - Version (text)
    - Sale_Date (text)
    - Customer_Name (text)
    - Customer_Country (text)
    - Sale_Amount (real)
    - Payment_Method (text)
    """

def generate_insight(user_query, sql_query, query_results):
    schema = get_table_schema()
    
    prompt = f"""
    Context:
    User Query: {user_query}
    SQL Query: {sql_query}
    Query Results: {query_results}
    {schema}

    Task: Analyze the query results and provide an insight to the user's original question using the data from the query result.  
    Keep the response concise and short.

    Response:
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
        temperature=0.5,
    )

    return response.choices[0].message.content

def main():
    while True:
        user_query = input("Enter your question (or 'quit' to exit): ")
        if user_query.lower() == 'quit':
            break
        
        sql_query = natural_language_to_sql(user_query)
        print(f"Generated SQL Query: {sql_query}")
        
        try:
            results = execute_sql_query(sql_query)
            print("Query Results:")
            for row in results:
                print(row)
            
            insight = generate_insight(user_query, sql_query, results)
            print("\nInsight:")
            print(insight)
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()