import sqlite3

# Function to create the database and sample data; run this script before running text_to_sql2
def create_sample_database():
    conn = sqlite3.connect('software_sales_database.db')  # Updated database name
    cursor = conn.cursor()

    # Create customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        Customer_ID INTEGER PRIMARY KEY,
        Customer_Name TEXT,
        Customer_Country TEXT,
        Email TEXT
    )
    ''')

    # Create software table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS software (
        Software_ID INTEGER PRIMARY KEY,
        Software_Name TEXT,
        Version TEXT,
        Release_Date TEXT
    )
    ''')

    # Create sales table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        Sale_ID INTEGER PRIMARY KEY,
        Software_ID INTEGER,
        Customer_ID INTEGER,
        Sale_Date TEXT,
        Sale_Amount REAL,
        Payment_Method TEXT,
        FOREIGN KEY (Software_ID) REFERENCES software (Software_ID),
        FOREIGN KEY (Customer_ID) REFERENCES customers (Customer_ID)
    )
    ''')

    # Sample data for customers
    customers_data = [
        (1, 'Alice Johnson', 'USA', 'alice@example.com'),
        (2, 'Bob Smith', 'Canada', 'bob@example.com'),
        (3, 'Charlie Brown', 'UK', 'charlie@example.com'),
        (4, 'David Wilson', 'Australia', 'david@example.com'),
        (5, 'Eva Green', 'Germany', 'eva@example.com'),
        (6, 'Frank Wright', 'France', 'frank@example.com'),
        (7, 'Grace Lee', 'Japan', 'grace@example.com'),
        (8, 'Henry Adams', 'USA', 'henry@example.com'),
        (9, 'Ivy Clark', 'Brazil', 'ivy@example.com'),
        (10, 'Jack White', 'India', 'jack@example.com'),
    ]

    # Sample data for software
    software_data = [
        (1, 'Software A', '1.0', '2022-01-01'),
        (2, 'Software B', '2.1', '2022-02-01'),
        (3, 'Software C', '3.0', '2022-03-01'),
        (4, 'Software D', '1.0', '2022-04-01'),
        (5, 'Software E', '1.0', '2022-05-01'),
        (6, 'Software F', '1.0', '2022-06-01'),
        (7, 'Software G', '2.0', '2022-07-01'),
        (8, 'Software H', '1.5', '2022-08-01'),
        (9, 'Software I', '3.1', '2022-09-01'),
        (10, 'Software J', '2.2', '2022-10-01'),
    ]

    # Sample data for sales
    sales_data = [
        (1, 1, 1, '2023-01-15', 199.99, 'Credit Card'),
        (2, 2, 2, '2023-02-20', 299.99, 'PayPal'),
        (3, 3, 3, '2023-03-10', 399.99, 'Debit Card'),
        (4, 1, 4, '2023-04-05', 199.99, 'Credit Card'),
        (5, 4, 5, '2023-05-15', 249.99, 'Bank Transfer'),
        (6, 2, 6, '2023-06-25', 299.99, 'Credit Card'),
        (7, 5, 7, '2023-07-30', 149.99, 'PayPal'),
        (8, 3, 8, '2023-08-12', 399.99, 'Debit Card'),
        (9, 6, 9, '2023-09-18', 199.99, 'Credit Card'),
        (10, 7, 10, '2023-10-22', 299.99, 'Bank Transfer'),
        (11, 8, 1, '2023-11-01', 199.99, 'Credit Card'),
        (12, 9, 2, '2023-11-15', 299.99, 'PayPal'),
        (13, 10, 3, '2023-12-01', 399.99, 'Debit Card'),
        (14, 1, 4, '2023-12-10', 199.99, 'Credit Card'),
        (15, 2, 5, '2023-12-20', 249.99, 'Bank Transfer'),
    ]

    # Insert sample data into tables
    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?)', customers_data)
    cursor.executemany('INSERT INTO software VALUES (?, ?, ?, ?)', software_data)
    cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?)', sales_data)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_sample_database()
