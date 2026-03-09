#!/usr/bin/env python3
"""
Test script to verify LLM connection
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

def test_llm_connection():
    """Test if LLM is working"""
    print("Testing LLM connection...")
    
    # Check environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    print(f"API Key: {'***' + api_key[-4:] if api_key and api_key != 'your_api_key_here' else 'Not set or default'}")
    print(f"Base URL: {base_url}")
    
    if not api_key or api_key == "your_api_key_here":
        print("X OPENAI_API_KEY is not configured properly")
        return False
    
    if not base_url:
        print("X OPENAI_BASE_URL is not configured")
        return False
    
    try:
        # Initialize OpenAI client
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        print("+ LLM initialized successfully")
        
        # Test a simple query
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": "Respond with 'LLM is working' if you can read this."}],
            temperature=0
        )
        
        print(f"+ LLM Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"X LLM connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_llm_connection()
    if success:
        print("\n+ LLM is working correctly!")
    else:
        print("\nX LLM connection failed. Please check your configuration.")
