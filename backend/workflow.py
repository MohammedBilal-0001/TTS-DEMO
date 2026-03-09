"""
LangGraph workflow definition for the AI Analytics System
"""
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from state import AnalyticsState
from agents import (
    router_agent, 
    text_to_sql_agent, 
    analyzer_agent, 
    visualizer_agent, 
    response_builder_agent
)
from tools import execute_sql_tool, retry_router, parallel_router, intent_router

def create_workflow() -> StateGraph:
    """Create the LangGraph workflow"""
    
    # Create the graph
    workflow = StateGraph(AnalyticsState)
    
    # Add nodes
    workflow.add_node("router", router_agent)
    workflow.add_node("text_to_sql", text_to_sql_agent)
    workflow.add_node("execute_sql", execute_sql_tool)
    workflow.add_node("analyzer", analyzer_agent)
    workflow.add_node("visualizer", visualizer_agent)
    workflow.add_node("response_builder", response_builder_agent)
    
    # Add edges
    workflow.set_entry_point("router")
    
    # Router to Text-to-SQL or Response Builder based on intent
    workflow.add_conditional_edges(
        "router",
        intent_router,
        {
            "text_to_sql": "text_to_sql",
            "response_builder": "response_builder"
        }
    )
    
    # Text-to-SQL to SQL Executor
    workflow.add_edge("text_to_sql", "execute_sql")
    
    # Conditional routing after SQL execution
    workflow.add_conditional_edges(
        "execute_sql",
        retry_router,
        {
            "retry": "text_to_sql",
            "success": "parallel_router",
            "fail": "response_builder"
        }
    )
    
    # Add parallel router node
    workflow.add_node("parallel_router", lambda state: state)  # Pass-through node
    
    # Route from success to parallel router
    workflow.add_edge("execute_sql", "parallel_router")
    
    # Parallel routing from parallel_router
    workflow.add_conditional_edges(
        "parallel_router",
        parallel_router,
        {
            "analyzer": "analyzer",
            "visualizer": "visualizer",
            "response_builder": "response_builder"
        }
    )
    
    # Both analyzer and visualizer go to response_builder
    workflow.add_edge("analyzer", "response_builder")
    workflow.add_edge("visualizer", "response_builder")
    
    # Response builder to end
    workflow.add_edge("response_builder", END)
    
    return workflow

def create_compiled_workflow():
    """Create and compile the workflow"""
    workflow = create_workflow()
    return workflow.compile()

# Global compiled workflow instance
compiled_workflow = create_compiled_workflow()
