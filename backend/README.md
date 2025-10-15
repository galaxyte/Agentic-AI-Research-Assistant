# Backend - Agentic AI Research Assistant

FastAPI backend with multi-agent AI orchestration using LangGraph and CrewAI.

## 🚀 Quick Start

### Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=sk-your-key-here
TAVILY_API_KEY=tvly-your-key-here
WEAVIATE_URL=http://localhost:8080
```

### Run Server

```bash
python main.py
```

Server runs on: `http://localhost:8000`

## 📚 API Documentation

Interactive docs: `http://localhost:8000/docs`

### Key Endpoints

- `GET /health` - Health check
- `POST /query` - Create research query
- `GET /stream/{task_id}` - Stream results (SSE)
- `GET /task/{task_id}` - Get task status

## 🧩 Agent Architecture

### Researcher Agent
**Role**: Web research specialist
- Searches Tavily API
- Queries Weaviate memory
- Ranks and filters results

### Summarizer Agent
**Role**: Information synthesis
- Condenses content
- Combines multiple sources
- Creates cohesive summaries

### Validator Agent
**Role**: Fact verification
- Extracts claims
- Cross-checks sources
- Assigns confidence scores

### Presenter Agent
**Role**: Response formatting
- Structures findings
- Formats markdown
- Streams output

## 🔧 Development

### Run with auto-reload

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### View logs

```bash
# Logs are output to console
# Adjust logging level in main.py
```

## 🧪 Testing

```bash
# Test health endpoint
curl http://localhost:8000/health

# Create query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is LangGraph?", "stream": true}'
```

## 📦 Dependencies

Main packages:
- `fastapi` - Web framework
- `langgraph` - Agent orchestration
- `openai` - GPT-4 access
- `weaviate-client` - Vector storage
- `tavily-python` - Web search
- `sse-starlette` - Streaming support

See `requirements.txt` for full list.

## 🔒 Security Notes

- Never commit `.env` file
- Keep API keys secure
- Use environment variables in production
- Enable CORS only for trusted origins

## 📖 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Guide](https://python.langchain.com/docs/langgraph)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

