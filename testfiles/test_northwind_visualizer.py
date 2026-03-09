#!/usr/bin/env python3
"""
Test visualizer with actual Northwind database data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from state import AnalyticsState, StateHelper
from agents import visualizer_agent
import sqlite3
import pandas as pd

def get_northwind_data():
    """Get actual data from Northwind database"""
    # Use the same database URL as in tools.py
    database_url = os.getenv('DATABASE_URL', 'sqlite:///D:/SQLLite/DataBases/northwind/northwind_simplified.db')
    if database_url.startswith('sqlite:///'):
        db_path = database_url[10:]
    else:
        db_path = database_url
    
    print(f"Connecting to database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    
    # First, let's see what tables exist
    tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables_df = pd.read_sql_query(tables_query, conn)
    print(f"Available tables: {tables_df['name'].tolist()}")
    
    # Test different queries that would work with Northwind
    queries = [
        "SELECT Region, COUNT(*) as customer_count FROM Customers GROUP BY Region",
        "SELECT Country, COUNT(*) as customer_count FROM Customers GROUP BY Country", 
        "SELECT CategoryName, COUNT(*) as product_count FROM Products p JOIN Categories c ON p.CategoryID = c.CategoryID GROUP BY CategoryName"
    ]
    
    test_data = []
    for query in queries:
        try:
            df = pd.read_sql_query(query, conn)
            if not df.empty:
                test_data.append((query, df))
                print(f"\nQuery: {query}")
                print(f"Data shape: {df.shape}")
                print(f"Columns: {df.columns.tolist()}")
                print(f"Sample data:\n{df.head()}")
        except Exception as e:
            print(f"Error with query '{query}': {e}")
    
    conn.close()
    return test_data

# Test different questions with real data
test_questions = [
    "Show customer count by region",
    "Show customer count by country", 
    "Show product count by category"
]

print("=== Testing Visualizer with Real Northwind Data ===\n")

# Get real data
real_data_samples = get_northwind_data()

if not real_data_samples:
    print("No data found. Check database connection and table names.")
    sys.exit(1)

# Test with real data
for i, (query, data) in enumerate(real_data_samples):
    if i < len(test_questions):
        question = test_questions[i]
        print(f"\n" + "="*60)
        print(f"Question: {question}")
        print(f"Using data from query: {query}")
        
        # Create state with question and real data
        state = StateHelper.initialize_state(question)
        state["query_result"] = data
        state["question"] = question
        
        # Run visualizer
        result = visualizer_agent(state)
        chart_spec = result["chart_spec"]
        
        print(f"\nChart Results:")
        print(f"Chart Type: {chart_spec.get('chart_type')}")
        print(f"X-axis: {chart_spec.get('x')}")
        print(f"Y-axis: {chart_spec.get('y')}")
        print(f"Title: {chart_spec.get('title')}")
        print(f"Actual data values being plotted:")
        for record in data.to_dict('records')[:5]:
            print(f"  {record}")
        print("-" * 50)
