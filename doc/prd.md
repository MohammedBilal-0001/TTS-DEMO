# Product Requirements Document

## AI Multi-Agent SQL Analytics System

Version: 1.0
Author: Project Owner
Purpose: Demo system for AI orchestration challenge

---

# 1. Product Overview

This project implements a **multi-agent AI analytics system** capable of:

1. Converting natural language questions into SQL queries.
2. Executing those queries on a database.
3. Analyzing the results.
4. Generating visualizations.
5. Returning insights to the user.

The system demonstrates **AI agent orchestration using LangGraph**.

It should clearly show:

* agent collaboration
* tool usage
* execution logs
* retry logic
* conditional routing
* parallel execution

The system is designed **for demonstration purposes** and uses a **static SQLite database schema**.

---

# 2. Key Goals

The system must demonstrate the following capabilities:

### Agent Orchestration

Multiple agents collaborate to complete a task.

### Tool Usage

Agents use external tools such as a SQL executor.

### Transparent Logs

Each agent step is logged and visible to the user.

### Error Recovery

The system automatically retries failed SQL queries.

### Parallel Agent Execution

Analysis and visualization agents run simultaneously.

---

# 3. Technology Stack

## Backend

Language:
Python 3.10+

Libraries:

FastAPI (API server)

LangGraph (agent orchestration)

SQLAlchemy (database connection)

Pandas (data manipulation)

Pydantic (state validation)

SQLite (database)

LLM access:

OpenAI compatible API through local LLM Studio endpoint.

---

## Frontend

Minimal interface similar to voice-assistant tools.

Framework: Next.js

Charts rendered using a frontend chart library.

The frontend should show:

* user input
* execution logs
* insights
* chart output

---

# 4. System Architecture

The system follows a **graph-based orchestration pipeline**.

Execution flow:

User Question
→ Router Agent
→ Text-to-SQL Agent
→ SQL Execution Tool
→ Retry Logic
→ Parallel Agents (Analyzer + Visualizer)
→ Response Builder
→ UI Output

---

# 5. LangGraph Workflow

Graph nodes:

Router
TextToSQL
ExecuteSQL
RetryRouter
ParallelRouter
Analyzer
Visualizer
ResponseBuilder

Graph structure:

START
→ Router
→ TextToSQL
→ ExecuteSQL
→ RetryRouter

RetryRouter routes:

retry → TextToSQL
success → ParallelRouter

ParallelRouter routes:

Analyzer
Visualizer

Both nodes return to:

ResponseBuilder → END

---

# 6. State Object Definition

The LangGraph state stores all information exchanged between agents.

Required fields:

question: original user question

intent: type of request

needs_analysis: boolean flag

needs_visualization: boolean flag

sql_query: generated SQL

query_result: dataframe from SQL execution

retry_count: current retry number

max_retries: maximum retries allowed

last_error: error message from failed SQL

insights: analysis output

chart_spec: visualization instructions

logs: list of execution log messages

---

# 7. Logging System

Every agent must log its activity.

Example log messages:

[Router] Intent detected: database_query

[TextToSQL] Generated SQL query

[Executor] Query executed successfully

[Analyzer] Generated insights

[Visualizer] Selected bar chart

Logs are stored in the state and returned to the UI.

---

# 8. Agents

## Router Agent

Purpose:
Classify the user request.

Outputs:

intent
needs_analysis
needs_visualization

Example output:

intent = "database_query"

needs_analysis = true

needs_visualization = true

---

## TextToSQL Agent

Purpose:
Convert natural language to SQL.

Input:

question
database schema
last_error (optional)

Output:

sql_query

Important requirement:
Return **only valid SQL**.

---

## SQL Executor Tool

Purpose:
Run SQL queries against SQLite database.

Implementation uses pandas:

pd.read_sql_query()

Output:
pandas DataFrame stored in state.

If an error occurs:

* capture exception
* store error in last_error
* increment retry_count

---

## Retry Router

Purpose:
Handle SQL execution failures.

Logic:

If last_error exists AND retry_count < max_retries
→ return "retry"

If retry_count >= max_retries
→ return "fail"

If no error
→ return "success"

Retry sends execution back to TextToSQL with the error appended to the prompt.

---

## Parallel Router

Purpose:
Decide which downstream agents should run.

Conditions:

needs_analysis → run Analyzer

needs_visualization → run Visualizer

Both agents can run simultaneously.

---

## Analyzer Agent

Purpose:
Interpret SQL query results.

Input:

query_result dataframe

Output:

insights string

Example output:

"The West region generated the highest revenue."

Data passed to LLM should be a **table preview** using dataframe.to_markdown().

Limit preview to 20 rows.

---

## Visualization Agent

Purpose:
Recommend a chart for the data.

Input:

query_result dataframe

Convert dataframe to JSON records.

Example output:

{
chart_type: "bar",
x: "region",
y: "revenue",
title: "Revenue by Region"
}

The frontend will render the chart.

---

## Response Builder

Purpose:
Merge agent outputs.

Combine:

insights
chart_spec
logs

Return final response.

---

# 9. SQL Retry Strategy

The system retries SQL generation if execution fails.

Maximum retries:

max_retries = 4

Retry process:

TextToSQL generates SQL

ExecuteSQL runs query

If error occurs:

RetryRouter sends execution back to TextToSQL

Prompt includes:

previous SQL query
error message
database schema

The LLM must correct the query.

---

# 10. Static Database Schema

The system uses a predefined schema.

Example schema:

orders table:

id INTEGER
product TEXT
region TEXT
revenue FLOAT
order_date DATE

customers table:

id INTEGER
name TEXT
region TEXT

This schema is injected into TextToSQL prompts.

---

# 11. Data Handling Strategy

The SQL executor stores the **full dataframe in state**.

Agents transform the data locally.

Analyzer receives:

markdown table preview.

Visualizer receives:

JSON records.

This improves:

analysis accuracy
visualization reliability
token efficiency.

---

# 12. Safety Rules

SQL execution must reject unsafe queries.

Disallowed keywords:

DROP
DELETE
UPDATE
INSERT
ALTER

If detected, the system stops execution.

---

# 13. API Endpoints

Backend exposes a single endpoint.

POST /query

Input:

user question

Output:

insights
chart_spec
logs

Example response:

{
"insights": "West region has highest revenue",
"chart_spec": {...},
"logs": [...]
}

---

# 14. Frontend Requirements

The frontend should display:

User input field

Execution logs panel

Insight output

Chart visualization

Layout sections:

User Input
Agent Logs
Insights
Chart

The logs should appear progressively to simulate agent reasoning.

---

# 15. Demo Scenarios

Example queries to test:

Show total revenue by region

Which product generates the most revenue?

Show revenue trends over time

Which region has the lowest sales?

These ensure SQL generation, analysis, and visualization all function correctly.

---

# 16. Success Criteria

The system is considered complete when:

User can ask a question in natural language.

System generates SQL.

SQL executes successfully.

Results are analyzed.

Visualization is generated.

Logs show the reasoning process.

Retry mechanism corrects SQL errors.

---

# 17. Future Improvements (Optional)

Dynamic schema retrieval

Multi-database support

Streaming token output

Memory for conversation history

Advanced visualization planning

---

End of Document
