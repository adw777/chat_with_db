import sqlite3
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from create_database import create_sample_database

# Load the model and tokenizer
model_path = 'gaussalgo/T5-LM-Large-text2sql-spider'
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

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
    # create_sample_database()
    
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