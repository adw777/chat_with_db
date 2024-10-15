from pymongo import MongoClient
from datetime import datetime, timedelta
import random

def create_sample_database():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['software_sales_database']

    # Create collections
    customers = db['customers']
    software = db['software']
    sales = db['sales']

    # Clear existing data
    customers.delete_many({})
    software.delete_many({})
    sales.delete_many({})

    # Sample data for customers
    customer_data = [
        {"_id": i, "name": f"Customer {i}", "country": random.choice(["USA", "Canada", "UK", "Germany", "France", "Japan", "Australia"]), "email": f"customer{i}@example.com"}
        for i in range(1, 1001)
    ]
    customers.insert_many(customer_data)

    # Sample data for software
    software_data = [
        {"_id": i, "name": f"Software {chr(64+i)}", "version": f"{random.randint(1,5)}.{random.randint(0,9)}", "release_date": (datetime.now() - timedelta(days=random.randint(1, 1000))).strftime("%Y-%m-%d")}
        for i in range(1, 101)
    ]
    software.insert_many(software_data)

    # Sample data for sales
    sale_data = []
    for i in range(1, 10001):
        sale_date = datetime.now() - timedelta(days=random.randint(1, 365))
        sale_data.append({
            "_id": i,
            "software_id": random.randint(1, 100),
            "customer_id": random.randint(1, 1000),
            "sale_date": sale_date.strftime("%Y-%m-%d"),
            "sale_amount": round(random.uniform(50, 1000), 2),
            "payment_method": random.choice(["Credit Card", "PayPal", "Bank Transfer", "Crypto"])
        })
    sales.insert_many(sale_data)

    print("Sample database created successfully!")

if __name__ == "__main__":
    create_sample_database()