#!/usr/bin/env python3
"""
Test script to debug LLM response
"""
from agents import llm
from langchain.schema import HumanMessage

# Test LLM response directly
prompt = """Analyze this user question and determine:
1. The intent (database_query, general_question, or other)
2. Whether data analysis is needed (true/false)
3. Whether visualization is needed (true/false)

User question: "Show total revenue by region"

Respond with JSON format:
{
    "intent": "database_query",
    "needs_analysis": true,
    "needs_visualization": true
}"""

response = llm.invoke([HumanMessage(content=prompt)])
print('Raw response content:')
print(repr(response.content))
print('Response content:')
print(response.content)

# Try to parse as JSON
import json
try:
    result = json.loads(response.content)
    print('Parsed JSON:', result)
except Exception as e:
    print('JSON parsing error:', e)
