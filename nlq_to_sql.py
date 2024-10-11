import sqlite3
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from groq import Groq

# Initialize the Groq client
groq_client = Groq()

def connect_to_database(db_path):
    """
    Connect to the SQLite database.
    
    Args:
    db_path (str): Path to the SQLite database file
    
    Returns:
    sqlite3.Connection: Database connection object
    """
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def convert_to_sql(query):
    """
    Convert natural language query to SQL using a pre-trained model.
    
    Args:
    query (str): Natural language query
    
    Returns:
    str: Generated SQL query
    """
    # Load pre-trained model and tokenizer
    model_name = "facebook/bart-large-cnn"  # You may want to use a more appropriate model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    # Tokenize and generate SQL
    inputs = tokenizer(query, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(**inputs, max_length=128)
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return sql_query

def execute_query(conn, sql_query):
    """
    Execute SQL query on the database.
    
    Args:
    conn (sqlite3.Connection): Database connection object
    sql_query (str): SQL query to execute
    
    Returns:
    list: Query results
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
        return None

def generate_answer(results, query):
    """
    Generate natural language answer using Groq's LLaMA 3.1 8B model.
    
    Args:
    results (list): Query results
    query (str): Original natural language query
    
    Returns:
    str: Generated natural language answer
    """
    # Prepare the prompt for the LLaMA model
    prompt = f"Query: {query}\nResults: {results}\nProvide insights about the data retrieved:"
    
    # Generate response using Groq's LLaMA 3.1 8B model
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides insights about data."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def nlq_to_sql_pipeline(query, db_path):
    """
    Main pipeline function that orchestrates the entire process.
    
    Args:
    query (str): Natural language query
    db_path (str): Path to the SQLite database file
    
    Returns:
    str: Generated natural language answer with insights
    """
    # Connect to the database
    conn = connect_to_database(db_path)
    if not conn:
        return "Failed to connect to the database."
    
    # Convert natural language query to SQL
    sql_query = convert_to_sql(query)
    
    # Execute the SQL query
    results = execute_query(conn, sql_query)
    if not results:
        return "Failed to execute the query or no results found."
    
    # Generate natural language answer
    answer = generate_answer(results, query)
    
    # Close the database connection
    conn.close()
    
    return answer

# Example usage
if __name__ == "__main__":
    db_path = "path/to/your/database.sqlite"
    user_query = "What are the top 5 selling products in the last month?"
    result = nlq_to_sql_pipeline(user_query, db_path)
    print(result)