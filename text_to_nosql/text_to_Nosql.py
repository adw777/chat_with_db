from pymongo import MongoClient
from groq import Groq
import ast

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

    Provide only the Python code to execute the MongoDB query using PyMongo. The code should return the query results as a list.
    Do not include any print statements or return statements. The code will be executed directly.
    """

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-8b-instant",
        max_tokens=500,
        temperature=0.2,
    )

    nosql_query = response.choices[0].message.content.strip()

    if nosql_query.startswith("```python"):
        nosql_query = nosql_query[len("```python"):].strip()
    if nosql_query.endswith("```"):
        nosql_query = nosql_query[:-3].strip()

    return nosql_query

def execute_nosql_query(nosql_query):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['software_sales_database']
    
    # Create a safe local environment for execution
    safe_env = {
        'db': db,
        'MongoClient': MongoClient,
    }
    
    try:
        # Parse the query into an AST
        parsed = ast.parse(nosql_query)
        
        # Ensure the last statement returns the result
        if isinstance(parsed.body[-1], ast.For):
            # If the last statement is a for loop, we'll collect its results
            collection_var = ast.Name(id='_result_collection', ctx=ast.Store())
            parsed.body.insert(-1, ast.Assign(targets=[collection_var], value=ast.List(elts=[], ctx=ast.Load())))
            parsed.body[-1].body.append(ast.Expr(ast.Call(func=ast.Attribute(value=collection_var, attr='append', ctx=ast.Load()), args=[parsed.body[-1].body[-1].value], keywords=[])))
            parsed.body.append(ast.Return(collection_var))
        elif not isinstance(parsed.body[-1], ast.Return):
            parsed.body.append(ast.Return(parsed.body[-1].value))
        
        # Compile and execute the modified AST
        code = compile(parsed, '<string>', 'exec')
        exec(code, safe_env)
        
        # The last executed statement should now be a return, giving us the result
        result = safe_env.get('_result_collection', None) or safe_env.get('result', None)
        
        if isinstance(result, dict):
            return [result]
        return list(result)
    except Exception as e:
        raise Exception(f"Error executing query: {e}")

def main():
    while True:
        user_query = input("Enter your question (or 'quit' to exit): ")
        if user_query.lower() == 'quit':
            break
        
        nosql_query = natural_language_to_nosql(user_query)
        print(f"Generated MongoDB Query:")
        print(nosql_query)
        
        try:
            results = execute_nosql_query(nosql_query)
            print("\nQuery Results:")
            for row in results[:5]:  # Print first 5 results
                print(row)
            print(f"\nTotal results: {len(results)}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()