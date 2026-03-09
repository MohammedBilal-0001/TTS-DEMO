#!/usr/bin/env python3
"""
Test the exact failing query
"""
import sqlite3
import os
import pandas as pd

# Use the same database path as the application
database_url = os.getenv('DATABASE_URL', 'sqlite:///D:/SQLLite/DataBases/northwind/northwind_simplified.db')
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
    
    # Try a simpler query to test the connection
    try:
        conn = sqlite3.connect(db_path)
        simple_sql = "SELECT * FROM OrderDetails LIMIT 5"
        result = pd.read_sql_query(simple_sql, conn)
        print(f"\nSimple query worked - {len(result)} rows from OrderDetails")
        print(result)
        conn.close()
    except Exception as e2:
        print(f"Simple query also failed: {e2}")
