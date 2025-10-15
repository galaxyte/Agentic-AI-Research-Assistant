# 🤖 Agentic AI Research Assistant

A sophisticated multi-agent AI research assistant that autonomously gathers, summarizes, validates, and presents information from the web using cutting-edge AI technologies.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)

## 🌟 Features

- **🧠 Multi-Agent Architecture**: Specialized AI agents working together
  - 🧑‍🔬 **Researcher**: Searches and extracts web content
  - ✍️ **Summarizer**: Condenses information into insights
  - ✅ **Validator**: Cross-verifies facts with confidence scores
  - 💬 **Presenter**: Structures and streams responses

- **🔄 Autonomous Orchestration**: LangGraph-based workflow management
- **🌐 Web Data Collection**: Real-time web search via Tavily API
- **🧠 Semantic Memory**: Weaviate vector store for context retention
- **✨ Real-Time Streaming**: Live progress updates via SSE
- **🎨 Modern UI**: Beautiful React interface with TailwindCSS
- **📊 Fact Validation**: Multi-source verification with confidence metrics

## 🏗️ Architecture

```
User Query → Researcher → Summarizer → Validator → Presenter → Stream Response
                ↓             ↓           ↓            ↓
            Weaviate Vector Store (Semantic Memory)
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **LangGraph**: Agent workflow orchestration
- **CrewAI**: Agent role management
- **OpenAI SDK**: GPT-4 for reasoning and generation
- **Weaviate**: Vector database for semantic memory
- **Tavily API**: Advanced web search
- **SSE**: Server-Sent Events for streaming

### Frontend
- **React.js + Vite**: Fast, modern web framework
- **TailwindCSS**: Utility-first styling
- **React Markdown**: Formatted response rendering
- **Axios**: HTTP client
- **EventSource**: SSE client

## 📦 Installation

### Prerequisites

- Python 3.9+
- Node.js 18+
- API Keys:
  - OpenAI API Key ([Get it here](https://platform.openai.com/api-keys))
  - Tavily API Key ([Get it here](https://tavily.com))
  - Optional: Weaviate instance (local or cloud)

### Quick Start

#### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd agentic-ai-research-assistant
```

#### 2️⃣ Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your API keys
```

**Configure `backend/.env`:**
```env
OPENAI_API_KEY=sk-your-openai-key
TAVILY_API_KEY=tvly-your-tavily-key
WEAVIATE_URL=http://localhost:8080
```

#### 3️⃣ Start Weaviate (Optional but Recommended)

Using Docker:
```bash
docker run -d \
  -p 8080:8080 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -e ENABLE_MODULES=text2vec-openai \
  -e OPENAI_APIKEY=your-openai-key \
  semitechnologies/weaviate:latest
```

Or use Weaviate Cloud Services (free tier available).

#### 4️⃣ Start Backend

```bash
# From backend directory
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

#### 5️⃣ Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## 🚀 Usage

1. **Access the Web Interface**: Open `http://localhost:3000` in your browser

2. **Ask a Question**: Type your research query in the input box
   - Example: "Explain the latest advancements in AI agent frameworks"

3. **Watch the Magic**: Observe real-time agent activity:
   - 🧑‍🔬 Researcher gathers web sources
   - ✍️ Summarizer creates insights
   - ✅ Validator checks facts
   - 💬 Presenter streams the response

4. **Review Results**: Get comprehensive answers with:
   - Main findings
   - Source citations
   - Confidence scores
   - Fact validation status

## 📖 API Documentation

### Endpoints

#### `GET /health`
Check backend health and service status

**Response:**
```json
{
  "status": "healthy",
  "weaviate": "connected",
  "openai": "configured",
  "tavily": "configured"
}
```

#### `POST /query`
Create a new research query

**Request:**
```json
{
  "query": "What are the benefits of multi-agent AI systems?",
  "stream": true
}
```

**Response:**
```json
{
  "task_id": "task_20240115_143022_123456",
  "status": "created",
  "message": "Research task created successfully"
}
```

#### `GET /stream/{task_id}`
Stream research progress and results (SSE)

**Events:**
- `status`: General status updates
- `stage`: Agent stage changes
- `log`: Agent activity logs
- `response`: Streamed response chunks
- `complete`: Research completion
- `error`: Error notifications

#### `GET /task/{task_id}`
Get task status

**Response:**
```json
{
  "task_id": "task_20240115_143022_123456",
  "status": "completed",
  "current_stage": "Completed",
  "final_response": "...",
  "error": ""
}
```

## 🔧 Configuration

### Environment Variables

#### Backend (`backend/.env`)

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | ✅ Yes |
| `TAVILY_API_KEY` | Tavily API key for web search | ✅ Yes |
| `WEAVIATE_URL` | Weaviate instance URL | ⚠️ Optional |
| `WEAVIATE_API_KEY` | Weaviate API key (if using cloud) | ⚠️ Optional |

#### Frontend (`frontend/.env`)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000` |

## 🎯 Project Structure

```
agentic-ai-research-assistant/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── agents/                 # AI agent implementations
│   │   ├── researcher.py       # Web research agent
│   │   ├── summarizer.py       # Summarization agent
│   │   ├── validator.py        # Fact validation agent
│   │   └── presenter.py        # Response presentation agent
│   ├── workflows/
│   │   └── research_graph.py   # LangGraph orchestration
│   ├── utils/
│   │   ├── weaviate_client.py  # Vector store client
│   │   ├── web_search.py       # Web search utility
│   │   ├── summarization.py    # Summarization utility
│   │   └── validation.py       # Fact validation utility
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatUI.jsx      # Main chat interface
│   │   │   └── MessageBubble.jsx # Message component
│   │   ├── App.jsx             # Root component
│   │   ├── api.js              # API client
│   │   └── index.css           # Global styles
│   ├── package.json            # Node dependencies
│   └── vite.config.js          # Vite configuration
│
└── README.md                   # This file
```

## 🧪 Example Queries

Try these questions to see the system in action:

1. **Technology Research**
   - "Explain the latest advancements in AI agent frameworks"
   - "Compare LangGraph, CrewAI, and AutoGen"

2. **General Knowledge**
   - "What are the main causes of climate change?"
   - "Explain quantum computing in simple terms"

3. **Current Events**
   - "What are the latest developments in renewable energy?"
   - "Summarize recent AI safety research"

4. **How-To Questions**
   - "How do I build a multi-agent AI system?"
   - "What are the best practices for prompt engineering?"

## 🔍 How It Works

### Agent Pipeline

1. **Researcher Agent** 🧑‍🔬
   - Searches Tavily API for relevant sources
   - Checks Weaviate for similar past queries
   - Extracts and ranks content

2. **Summarizer Agent** ✍️
   - Processes top sources
   - Creates concise summaries
   - Synthesizes information

3. **Validator Agent** ✅
   - Extracts key factual claims
   - Cross-verifies each claim
   - Assigns confidence scores

4. **Presenter Agent** 💬
   - Structures final response
   - Formats with markdown
   - Streams to user

### Workflow Orchestration

```python
# LangGraph defines the flow
workflow = StateGraph(ResearchState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("summarizer", summarizer_node)
workflow.add_node("validator", validator_node)
workflow.add_node("presenter", presenter_node)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "summarizer")
workflow.add_edge("summarizer", "validator")
workflow.add_edge("validator", "presenter")
workflow.add_edge("presenter", END)
```

## 🐛 Troubleshooting

### Backend won't start
- Verify Python 3.9+ is installed
- Check that all API keys are set in `.env`
- Ensure port 8000 is available

### Frontend can't connect
- Verify backend is running on port 8000
- Check browser console for CORS errors
- Ensure `VITE_API_URL` points to correct backend URL

### Weaviate connection failed
- Verify Weaviate is running on port 8080
- Check Docker container status
- System will work without Weaviate (no semantic memory)

### No search results
- Verify `TAVILY_API_KEY` is valid
- Check internet connection
- Review backend logs for API errors

## 📝 License

MIT License - feel free to use this project for learning and development!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 and embeddings
- **LangChain/LangGraph** for agent orchestration
- **Tavily** for web search API
- **Weaviate** for vector storage
- **CrewAI** for agent framework inspiration

## 📧 Support

For questions and support, please open an issue on GitHub.

---

**Built with ❤️ using cutting-edge AI technologies**

