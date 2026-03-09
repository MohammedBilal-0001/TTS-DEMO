"""
LangGraph agents for the AI Analytics System
"""
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from state import AnalyticsState, StateHelper
import json
import os

# Initialize LLM with environment variables - using safe initialization
try:
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY", "sk-not-needed"),
        base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:1234/v1")
    )
    # Create a simple wrapper for LangChain compatibility
    class SimpleLLM:
        def __init__(self, client, model="google/gemma-3-4b"):
            self.client = client
            self.model = model
        
        def invoke(self, messages):
            # Convert LangChain messages to OpenAI format
            openai_messages = []
            for msg in messages:
                if hasattr(msg, 'content'):
                    openai_messages.append({"role": "user", "content": msg.content})
                else:
                    openai_messages.append({"role": "user", "content": str(msg)})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                temperature=0
            )
            
            # Create a simple response object with content attribute
            class SimpleResponse:
                def __init__(self, content):
                    self.content = content
            
            return SimpleResponse(response.choices[0].message.content)
    
    llm = SimpleLLM(client)
    print("LLM initialized successfully")
except Exception as e:
    print(f"Warning: Could not initialize LLM - {e}")
    llm = None

def router_agent(state: AnalyticsState) -> AnalyticsState:
    """Classify the user request and determine what processing is needed"""
    
    print(f"[Router] Analyzing user question: {state['question']}")
    
    if llm is None:
        print("[Router] LLM not available - cannot proceed")
        return {
            "intent": "error",
            "needs_analysis": False,
            "needs_visualization": False
        }
    
    prompt = f"""
    Analyze this user question and determine:
    1. The intent (database_query, general_question, or other)
    2. Whether data analysis is needed (true/false)
    3. Whether visualization is needed (true/false)
    
    Guidelines:
    - Use "database_query" ONLY for questions asking about data, tables, records, statistics, or analysis from a database
    - Use "general_question" for conversational questions, greetings, personal questions, or non-data-related queries
    - Use "other" for unclear or unsupported requests
    - If "report" is mentioned, set data analysis & visualization TO TRUE
    
    Examples:
    "how are u today?" -> general_question, false, false
    "show me sales data" -> database_query, true, true
    "what's the weather?" -> general_question, false, false
    
    User question: "{state["question"]}"
    
    Respond with JSON format:
    {{
        "intent": "database_query",
        "needs_analysis": true,
        "needs_visualization": true
    }}
    """
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()
        
        # Clean up the response - remove markdown formatting
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()
        
        result = json.loads(content)
        
        intent = result.get("intent", "database_query")
        needs_analysis = result.get("needs_analysis", True)
        needs_visualization = result.get("needs_visualization", True)
        
        print(f"[Router] Intent detected: {intent}")
        print(f"[Router] Analysis needed: {needs_analysis}")
        print(f"[Router] Visualization needed: {needs_visualization}")
        
        return {
            "intent": intent,
            "needs_analysis": needs_analysis,
            "needs_visualization": needs_visualization
        }
        
    except Exception as e:
        print(f"[Router] Error: {str(e)}")
        return {
            "intent": "error",
            "needs_analysis": False,
            "needs_visualization": False
        }

def text_to_sql_agent(state: AnalyticsState) -> AnalyticsState:
    """Convert natural language to SQL query"""
    
    print("[TextToSQL] Converting question to SQL")
    
    if llm is None:
        print("[TextToSQL] LLM not available - cannot proceed")
        return {"current_sql": "", "sql_queries": [""]}
    
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from database.setup import get_database_schema
    
    schema = get_database_schema()
    
    if state.get("last_error"):
        prompt = f"""
        Convert this question to SQL. Your previous query failed.
        
        Question: "{state['question']}"
        
        Previous query: "{state['current_sql']}"
        
        Error: "{state['last_error']}"
        
        {schema}
        
        Generate a corrected SQL query. Return ONLY the SQL query, no explanations.
        """
    else:
        prompt = f"""
        Convert this question to SQL:
        
        Question: "{state['question']}"
        
        {schema}
        
        Generate a SQL query. Return ONLY the SQL query, no explanations.
        """
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        sql_query = response.content.strip()
        
        # Clean up the response - remove any markdown formatting
        if sql_query.startswith("```sql"):
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        elif sql_query.startswith("```"):
            sql_query = sql_query.replace("```", "").strip()
        
        # Normalize whitespace - replace newlines and multiple spaces with single spaces
        sql_query = ' '.join(sql_query.split())
        
        print(f"[TextToSQL] Generated SQL: {sql_query}")
        
        # Return with proper state structure
        return {
            "sql_queries": [sql_query],  # Add to history
            "current_sql": sql_query     # Set as current
        }
        
    except Exception as e:
        print(f"[TextToSQL] Error: {str(e)}")
        return {"current_sql": "", "sql_queries": [""]}

def analyzer_agent(state: AnalyticsState) -> AnalyticsState:
    """Analyze SQL query results and generate insights"""
    
    print("[Analyzer] Processing query results")
    
    if state.get("query_result") is None or state["query_result"].empty:
        print("[Analyzer] No data to analyze")
        return {"insights": "No data available for analysis."}
    
    if llm is None:
        print("[Analyzer] LLM not available - cannot proceed")
        return {"insights": "Analysis unavailable - LLM not connected"}
    
    table_preview = StateHelper.get_table_preview(state)
    
    prompt = f"""
    Analyze this data and provide insights:
    
    Question: "{state['question']}"
    
    Data:
    {table_preview}
    
    Provide a concise analysis of what this data shows. Focus on key patterns, trends, or insights.
    Keep your response to 1-2 sentences.
    """
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        print(f"[Analyzer] Generated insights")
        return {"insights": response.content.strip()}
        
    except Exception as e:
        print(f"[Analyzer] Error: {str(e)}")
        return {"insights": "Unable to analyze the data."}

def visualizer_agent(state: AnalyticsState) -> AnalyticsState:
    """Recommend a chart type for the data"""
    
    print("[Visualizer] Determining chart type")
    
    if state.get("query_result") is None or state["query_result"].empty:
        print("[Visualizer] No data to visualize")
        return {"chart_spec": {"chart_type": "none", "title": "No data available"}}
    
    if llm is None:
        print("[Visualizer] LLM not available - cannot proceed")
        return {"chart_spec": {"chart_type": "none", "title": "Visualization unavailable - LLM not connected"}}
    
    # Get data info
    columns = state["query_result"].columns.tolist()
    json_data = StateHelper.get_json_data(state)[:10]  # First 10 rows for analysis
    
    prompt = f"""
    Analyze this data and recommend the best chart type:
    
    Question: "{state['question']}"
    
    Columns: {columns}
    
    Sample data: {json.dumps(json_data, indent=2)}
    
    Recommend a chart type from: bar, line, pie, scatter
    
    Return JSON format:
    {{
        "chart_type": "bar",
        "x": "column_name",
        "y": "column_name", 
        "title": "Chart Title"
    }}
    
    For pie charts, only include "x" and "title".
    For scatter plots, include "x", "y", and "title".
    """
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()
        
        # Clean up the response - remove any markdown formatting
        if content.startswith("```json"):
            content = content.replace("```json", "").replace("```", "").strip()
        elif content.startswith("```"):
            content = content.replace("```", "").strip()
        
        # Try to find JSON content if there's extra text
        import re
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group(0)
        
        chart_spec = json.loads(content)
        chart_spec["data"] = StateHelper.get_json_data(state)  # Add actual data
        print(f"[Visualizer] Selected {chart_spec.get('chart_type', 'unknown')} chart")
        return {"chart_spec": chart_spec}
        
    except Exception as e:
        print(f"[Visualizer] Error: {str(e)}")
        print(f"[Visualizer] Raw response: {response.content[:200]}...")
        fallback_spec = {"chart_type": "bar", "title": "Data Visualization"}
        if state.get("query_result") is not None:
            fallback_spec["data"] = StateHelper.get_json_data(state)
        return {"chart_spec": fallback_spec}

def response_builder_agent(state: AnalyticsState) -> AnalyticsState:
    """Merge agent outputs into final response"""
    
    print("[ResponseBuilder] Creating final response")
    
    intent = state.get("intent", "database_query")
    
    # Handle general questions with conversational responses
    if intent == "general_question":
        question = state.get("question", "")
        
        # Simple conversational response logic
        if "how are" in question.lower() or "how r" in question.lower():
            response = "I'm doing well, thank you for asking! I'm here to help you with data analysis and SQL queries. Is there any data you'd like me to help you analyze?"
        elif "hello" in question.lower() or "hi" in question.lower() or "hey" in question.lower():
            response = "Hello! I'm ready to help you with data analysis and SQL queries. What would you like to explore today?"
        elif "thank" in question.lower() or "thanks" in question.lower():
            response = "You're welcome! Let me know if you need any help with your data analysis."
        else:
            response = "I'm here to help you with data analysis and SQL queries. Could you please ask me about your data or database?"
        
        print("[ResponseBuilder] Response complete")
        return {
            "insights": response,
            "chart_spec": {"chart_type": "none", "title": "Conversation"}
        }
    
    # Ensure all required fields exist for database queries
    insights = state.get("insights", "No insights generated.")
    chart_spec = state.get("chart_spec", {"chart_type": "none", "title": "No visualization"})
    
    print("[ResponseBuilder] Response complete")
    
    # Return only the final merged output
    return {
        "insights": insights,
        "chart_spec": chart_spec
    }
