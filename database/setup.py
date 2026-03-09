"""
Database setup for the AI Analytics System
"""
import sqlite3
import os
import json
from datetime import datetime, timedelta
import random

def create_database():
    """Create SQLite database with sample data"""
    
    # Ensure database directory exists
    os.makedirs('database', exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect('database/analytics.db')
    cursor = conn.cursor()
    
    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            product TEXT NOT NULL,
            region TEXT NOT NULL,
            revenue REAL NOT NULL,
            order_date DATE NOT NULL
        )
    ''')
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            region TEXT NOT NULL
        )
    ''')
    
    # Clear existing data
    cursor.execute('DELETE FROM orders')
    cursor.execute('DELETE FROM customers')
    
    # Sample data
    products = ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard', 'Mouse', 'Headphones', 'Speaker']
    regions = ['North', 'South', 'East', 'West']
    
    # Generate sample orders
    orders_data = []
    for i in range(1, 101):  # 100 sample orders
        product = random.choice(products)
        region = random.choice(regions)
        revenue = round(random.uniform(100, 5000), 2)
        order_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
        
        orders_data.append((i, product, region, revenue, order_date))
    
    cursor.executemany('INSERT INTO orders (id, product, region, revenue, order_date) VALUES (?, ?, ?, ?, ?)', orders_data)
    
    # Generate sample customers
    customers_data = []
    for i in range(1, 51):  # 50 sample customers
        name = f'Customer {i}'
        region = random.choice(regions)
        customers_data.append((i, name, region))
    
    cursor.executemany('INSERT INTO customers (id, name, region) VALUES (?, ?, ?)', customers_data)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print("Database created successfully with sample data!")

def get_database_schema():
    """Return the database schema as a string for LLM prompts"""
    try:
        # Read schema from text file with absolute path
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.txt')
        with open(schema_path, 'r') as f:
            schema_content = f.read()
        return schema_content
    except Exception as e:
        print(f"Warning: Could not load schema from file: {e}")
        # Fallback to basic schema
        return """
DATABASE SCHEMA:

Table: orders
- id (INTEGER, PRIMARY KEY) - Unique order identifier
- product (TEXT) - Product name
- region (TEXT) - Sales region (North, South, East, West)  
- revenue (REAL) - Revenue amount in USD
- order_date (DATE) - Order date in YYYY-MM-DD format

Table: customers
- id (INTEGER, PRIMARY KEY) - Unique customer identifier
- name (TEXT) - Customer name
- region (TEXT) - Customer region (North, South, East, West)

SQLite Notes:
- Use STRFTIME('%Y', order_date) to extract year from date
- Use STRFTIME('%m', order_date) to extract month from date
- Use STRFTIME('%Y-%m', order_date) to get year-month
"""

if __name__ == "__main__":
    create_database()
