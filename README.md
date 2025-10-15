# 🤖 Agentic AI Research Assistant

A sophisticated multi-agent AI research assistant that autonomously gathers, summarizes, validates, and presents information from the web using cutting-edge AI technologies.


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

#### Clone the Repository

```bash
git clone <your-repo-url>
cd agentic-ai-research-assistant
```

#### Backend Setup

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


Or use Weaviate Cloud Services (free tier available).

#### Start Backend

```bash
# From backend directory
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

#### Frontend Setup

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

