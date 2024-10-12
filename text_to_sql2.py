import sqlite3
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Load the model and tokenizer
model_path = 'gaussalgo/T5-LM-Large-text2sql-spider'
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Function to create the database and sample data
def create_sample_database():
    conn = sqlite3.connect('music_database.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS singer (
        Singer_ID INTEGER PRIMARY KEY,
        Name TEXT,
        Country TEXT,
        Song_Name TEXT,
        Song_release_year TEXT,
        Age INTEGER,
        Is_male BOOLEAN
    )
    ''')

    # Insert sample data
    sample_data = [
        (1, 'John Doe', 'USA', 'American Song', '2020', 35, True),
        (2, 'Jane Smith', 'France', 'French Melody', '2019', 28, False),
        (3, 'Pierre Dupont', 'France', 'Chanson d\'amour', '2021', 45, True),
        (4, 'Marie Claire', 'France', 'La vie en rose', '2018', 32, False),
    ]

    cursor.executemany('INSERT INTO singer VALUES (?, ?, ?, ?, ?, ?, ?)', sample_data)
    conn.commit()
    conn.close()

# Function to convert natural language to SQL
def natural_language_to_sql(question):
    schema = """
    "singer" "Singer_ID" int , "Name" text , "Country" text , "Song_Name" text , "Song_release_year" text , "Age" int , "Is_male" bool , foreign_key:  primary key: "Singer_ID"
    """

    input_text = f"Question: {question} Schema: {schema}"

    model_inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**model_inputs, max_length=512)

    sql_query = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return sql_query

# Function to execute SQL query
def execute_sql_query(sql_query):
    conn = sqlite3.connect('music_database.db')
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    return results

# Main function
def main():
    create_sample_database()
    
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