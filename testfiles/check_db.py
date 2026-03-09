#!/usr/bin/env python3
"""
Check what tables exist in the Northwind database
"""
import sqlite3
import os

# Use the same database path as the application
database_url = os.getenv('DATABASE_URL', 'sqlite:///D:/SQLLite/DataBases/northwind/northwind_simplified.db')
if database_url.startswith('sqlite:///'):
    db_path = database_url[10:]
else:
    db_path = database_url

print(f"Database path: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Tables in database:")
    for table in tables:
        print(f"- {table[0]}")
    
    # Get schema for each table
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        print(f"\n{table_name} columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
