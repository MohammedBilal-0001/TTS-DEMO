#!/usr/bin/env python3
"""
Test database connection exactly like the workflow does
"""
import sqlite3
import os
import pandas as pd

# Load environment variable like the workflow does
from dotenv import load_dotenv
load_dotenv()

print(f"DATABASE_URL from env: {os.getenv('DATABASE_URL')}")

# Use the same database path as the workflow
database_url = os.getenv('DATABASE_URL', 'sqlite:///C:/Users/USER/Desktop/Projects/Text-to-SQL-orc/database/analytics.db')
print(f"Database URL: {database_url}")

if database_url.startswith('sqlite:///'):
    db_path = database_url[10:]
else:
    db_path = database_url

print(f"Database path: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    
    # Test the exact failing query
    sql = "SELECT Customers.Country AS region, SUM(OrderDetails.UnitPrice * OrderDetails.Quantity) AS total_revenue FROM Customers JOIN Orders ON Customers.CustomerID = Orders.CustomerID JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID GROUP BY Customers.Country;"
    
    print(f"Testing query: {sql}")
    
    result = pd.read_sql_query(sql, conn)
    print(f"Success! Found {len(result)} rows:")
    print(result.head())
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
