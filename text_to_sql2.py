import sqlite3
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from create_database import create_sample_database

# Load the model and tokenizer
model_path = 'gaussalgo/T5-LM-Large-text2sql-spider'
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

def natural_language_to_sql(question):
    schema = """
    "customers" "Customer_ID" int, "Customer_Name" text, "Customer_Country" text, "Email" text, primary key: "Customer_ID";
    "software" "Software_ID" int, "Software_Name" text, "Version" text, "Release_Date" text, primary key: "Software_ID";
    "sales" "Sale_ID" int, "Software_ID" int, "Customer_ID" int, "Sale_Date" text, "Sale_Amount" real, "Payment_Method" text, primary key: "Sale_ID", foreign key: "Software_ID" references software (Software_ID), foreign key: "Customer_ID" references customers (Customer_ID);
    """

    input_text = f"Question: {question} Schema: {schema}"
    #input_text = " ".join(["Question: ",question, "Schema:", schema])

    model_inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**model_inputs, max_length=512)

    sql_query = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    # Ensure no leading commas or unwanted characters
    if sql_query.startswith(','):
        sql_query = sql_query[1:]  # Remove leading comma if present
    return sql_query

def execute_sql_query(sql_query):
    conn = sqlite3.connect('software_sales_database.db')
    cursor = conn.cursor()
    cursor.execute(sql_query)
    results = cursor.fetchall()
    conn.close()
    return results
"""
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
"""
