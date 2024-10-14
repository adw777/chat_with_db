import sqlite3

# Function to create the database and sample data; run this script before running text_to_sql2
def create_sample_database():
    conn = sqlite3.connect('software_sales_database.db')  # Updated database name
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        Sale_ID INTEGER PRIMARY KEY,
        Software_Name TEXT,
        Version TEXT,
        Sale_Date TEXT,
        Customer_Name TEXT,
        Customer_Country TEXT,
        Sale_Amount REAL,
        Payment_Method TEXT
    )
    ''')

    sample_data = [
        (1, 'Software A', '1.0', '2023-01-15', 'Alice Johnson', 'USA', 199.99, 'Credit Card'),
        (2, 'Software B', '2.1', '2023-02-20', 'Bob Smith', 'Canada', 299.99, 'PayPal'),
        (3, 'Software C', '3.0', '2023-03-10', 'Charlie Brown', 'UK', 399.99, 'Debit Card'),
        (4, 'Software A', '1.1', '2023-04-05', 'David Wilson', 'Australia', 199.99, 'Credit Card'),
        (5, 'Software D', '1.0', '2023-05-15', 'Eva Green', 'Germany', 249.99, 'Bank Transfer'),
        (6, 'Software B', '2.2', '2023-06-25', 'Frank Wright', 'France', 299.99, 'Credit Card'),
        (7, 'Software E', '1.0', '2023-07-30', 'Grace Lee', 'Japan', 149.99, 'PayPal'),
        (8, 'Software C', '3.1', '2023-08-12', 'Henry Adams', 'USA', 399.99, 'Debit Card'),
        (9, 'Software F', '1.0', '2023-09-18', 'Ivy Clark', 'Brazil', 199.99, 'Credit Card'),
        (10, 'Software G', '2.0', '2023-10-22', 'Jack White', 'India', 299.99, 'Bank Transfer'),
    ]

    cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?, ?)', sample_data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_sample_database()
