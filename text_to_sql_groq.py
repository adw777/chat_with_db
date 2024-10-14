import sqlite3
from groq import Groq
from create_database import create_sample_database

# Initialize Groq client
client = Groq()

def natural_language_to_sql(question):
    schema = """
    Table: customers
    Columns:
    - Customer_ID (int, primary key)
    - Customer_Name (text)
    - Customer_Country (text)
    - Email (text)

    Table: software
    Columns:
    - Software_ID (int, primary key)
    - Software_Name (text)
    - Version (text)
    - Release_Date (text)

    Table: sales
    Columns:
    - Sale_ID (int, primary key)
    - Software_ID (int, foreign key references software(Software_ID))
    - Customer_ID (int, foreign key references customers(Customer_ID))
    - Sale_Date (text)
    - Sale_Amount (real)
    - Payment_Method (text)
    """

    prompt = f"""
    Given the following database schema:

    {schema}

    Generate a SQL query to answer the following question:
    {question}

    Provide only the SQL query without any additional explanation.
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

    sql_query = response.choices[0].message.content.strip()
    
     # Remove unwanted ```sql and ``` from the start and end of the query
    if sql_query.startswith('```sql'):
        sql_query = sql_query[6:].strip()  # Remove the starting ```sql
    if sql_query.endswith('```'):
        sql_query = sql_query[:-3].strip()  # Remove the ending ```

    return sql_query

def execute_sql_query(sql_query):
    conn = sqlite3.connect('software_sales_database.db')
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    return results

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
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()