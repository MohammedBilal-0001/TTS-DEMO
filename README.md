# AI Multi-Agent SQL Analytics System

A demonstration system that showcases AI agent orchestration using LangGraph for natural language to SQL conversion, data analysis, and visualization.

## Features

- **Multi-Agent Architecture**: Router, Text-to-SQL, Analyzer, Visualizer, and Response Builder agents
- **LangGraph Workflow**: Agent orchestration with conditional routing and parallel execution
- **Natural Language to SQL**: Convert user questions into SQL queries automatically
- **Data Analysis**: AI-powered insights from query results
- **Visualization**: Automatic chart recommendations and rendering
- **Retry Logic**: Automatic SQL query correction on execution failures
- **Transparent Logging**: Real-time agent execution logs
- **Safety Checks**: SQL injection prevention and query validation

## Technology Stack

### Backend
- **Python 3.10+**
- **FastAPI**: REST API server
- **LangGraph**: Agent orchestration framework
- **LangChain**: LLM integration
- **LangChain OpenAI**: OpenAI-compatible API integration
- **SQLAlchemy**: Database ORM
- **Pandas**: Data manipulation
- **Pydantic**: State validation
- **SQLite**: Database
- **Uvicorn**: ASGI server
- **Python-dotenv**: Environment variable management

### Frontend
- **Next.js 14**: React framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Recharts**: Chart library
- **Lucide React**: Icons
- **Axios**: HTTP client

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- OpenAI-compatible API endpoint (e.g., LM Studio, Ollama) running on `http://localhost:1234/v1`

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the backend server:
```bash
python backend/server.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

1. Open the frontend in your browser
2. Type a natural language question about your data, for example:
   - "Show total revenue by region"
   - "Which product generates the most revenue?"
   - "Show revenue trends over time"
3. Click "Analyze" to process the query
4. Watch the agent logs in real-time
5. View the generated insights and visualizations

## API Endpoints

### `POST /query`
Process a natural language query.

**Request:**
```json
{
  "question": "Show total revenue by region"
}
```

**Response:**
```json
{
  "insights": "The West region generated the highest revenue.",
  "chart_spec": {
    "chart_type": "bar",
    "x": "region",
    "y": "revenue",
    "title": "Revenue by Region"
  },
  "query_results": {},
  "logs": ["[Router] Intent detected: database_query", ...],
  "success": true,
  "error": ""
}
```

### `GET /health`
Health check endpoint.

### `GET /demo-questions`
Get list of demo questions for testing.

## Architecture

### LangGraph Workflow

The system follows a graph-based orchestration pipeline:

1. **Router Agent**: Classifies user request and determines processing needs
2. **Text-to-SQL Agent**: Converts natural language to SQL query
3. **SQL Executor Tool**: Executes query with safety checks
4. **Retry Router**: Handles SQL execution failures with retry logic
5. **Parallel Router**: Determines which downstream agents to run
6. **Analyzer Agent**: Generates insights from query results
7. **Visualizer Agent**: Recommends chart types and specifications
8. **Response Builder**: Merges all outputs into final response

### State Management

The `AnalyticsState` object contains:
- User question and intent
- Generated SQL query
- Query results (pandas DataFrame)
- Analysis insights
- Chart specifications
- Execution logs
- Retry state

### Safety Features

- SQL injection prevention
- Query validation (SELECT only)
- Unsafe keyword blocking
- Maximum retry limits
- Error handling and logging

## Database Schema

The system uses a predefined SQLite schema with sample data:

**Orders Table:**
- id (INTEGER, PRIMARY KEY)
- product (TEXT)
- region (TEXT)
- revenue (REAL)
- order_date (DATE)

**Customers Table:**
- id (INTEGER, PRIMARY KEY)
- name (TEXT)
- region (TEXT)

## Development

### Project Structure
```
Text-to-SQL-orc/
├── backend/
│   ├── state.py          # LangGraph state definition
│   ├── state_simple.py   # Simplified state implementation
│   ├── agents.py         # AI agents
│   ├── tools.py          # SQL executor and routing logic
│   ├── workflow.py       # LangGraph workflow
│   └── server.py         # FastAPI server
├── database/
│   ├── schema.json       # Database schema definition
│   ├── analytics.db      # SQLite database file
│   └── northwind_simplified.db  # Sample database
├── frontend/
│   └── src/
│       ├── app/          # Next.js app
│       └── components/   # React components
├── testfiles/            # Test and debugging scripts
├── Analysis/             # Project analysis documents
├── Research/             # Research and documentation
├── Report/               # Project reports
├── doc/
│   └── prd.md           # Product Requirements Document
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md
```

### Adding New Agents

1. Create agent function in `backend/agents.py`
2. Add node to workflow in `backend/workflow.py`
3. Update routing logic as needed

### Extending Chart Types

1. Add new chart type to `frontend/src/components/ChartVisualization.tsx`
2. Update visualizer agent prompt in `backend/agents.py`

## Demo Recording

Watch a complete demonstration of the system in action:

**[View Demo Recording](https://drive.google.com/file/d/1077emmUWlgY8so55SxMnuHHBjU4PgXTj/view?usp=sharing)**

## Demo Scenarios

Test the system with these example queries:

- "Show total revenue by region"
- "Which product generates the most revenue?"
- "Show revenue trends over time"
- "Which region has the lowest sales?"
- "What are the top 3 products by revenue?"
- "How many orders were placed in each region?"
- "What is the average order value?"
- "Show customer distribution by region"

## Future Improvements

- Dynamic schema retrieval
- Multi-database support
- Streaming token output
- Conversation history memory
- Advanced visualization planning
- User authentication
- Query history
- Export functionality

## License

This project is for demonstration purposes only.
