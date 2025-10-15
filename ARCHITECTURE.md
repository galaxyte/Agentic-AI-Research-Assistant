# 🏗️ Architecture Overview

This document provides a detailed explanation of the Agentic AI Research Assistant's architecture, design decisions, and data flow.

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          React Frontend (Port 3000)                  │   │
│  │  • Chat UI                                           │   │
│  │  • SSE Client                                        │   │
│  │  • Markdown Renderer                                 │   │
│  └──────────────────┬──────────────────────────────────┘   │
└─────────────────────┼──────────────────────────────────────┘
                      │
                      │ HTTP/SSE
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                     │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              LangGraph Orchestration                  │  │
│  │                                                        │  │
│  │   ┌────────────┐   ┌────────────┐   ┌────────────┐  │  │
│  │   │ Researcher │──▶│ Summarizer │──▶│ Validator  │  │  │
│  │   └────────────┘   └────────────┘   └────────────┘  │  │
│  │         │                 │                 │         │  │
│  │         │                 │                 │         │  │
│  │         ▼                 ▼                 ▼         │  │
│  │   ┌────────────────────────────────────────────┐    │  │
│  │   │            Presenter Agent                  │    │  │
│  │   └────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
│                      │           │                           │
└──────────────────────┼───────────┼──────────────────────────┘
                       │           │
        ┌──────────────┘           └──────────────┐
        │                                          │
        ▼                                          ▼
┌──────────────────┐                    ┌──────────────────┐
│   Tavily API     │                    │  Weaviate Vector │
│  (Web Search)    │                    │  Database (8080) │
│                  │                    │                  │
│  • Search web    │                    │  • Embeddings    │
│  • Rank sources  │                    │  • Similarity    │
│  • Extract text  │                    │  • Memory store  │
└──────────────────┘                    └──────────────────┘
        │
        ▼
┌──────────────────┐
│   OpenAI API     │
│                  │
│  • GPT-4         │
│  • Embeddings    │
│  • Streaming     │
└──────────────────┘
```

## 🔄 Request Flow

### 1. User Submits Query

```
User → Frontend → POST /query → Backend
```

**Frontend:**
- User types question in chat input
- Input validated (non-empty)
- Creates query request
- Shows loading state

**Backend:**
- Generates unique task_id
- Initializes state
- Returns task_id to frontend

### 2. Stream Connection Established

```
Frontend → GET /stream/{task_id} → Backend → SSE Stream
```

**Frontend:**
- Opens EventSource connection
- Listens for multiple event types:
  - `status`: General updates
  - `stage`: Agent transitions
  - `log`: Agent activity
  - `response`: Answer chunks
  - `complete`: Finish signal
  - `error`: Error messages

**Backend:**
- Accepts SSE connection
- Starts LangGraph workflow
- Streams events as they occur

### 3. Agent Pipeline Execution

#### Stage 1: Researcher Agent 🧑‍🔬

```python
Input: { query: "User's question" }
↓
1. Check Weaviate for similar past queries
2. Search Tavily API for web results
3. Rank and filter sources
↓
Output: { research_results: [...], memory_context: "..." }
```

**What it does:**
- Queries vector database for semantic similarity
- Searches web using Tavily API
- Extracts top 10 most relevant sources
- Returns structured results

**Data structure:**
```python
{
    "title": "Source Title",
    "url": "https://...",
    "content": "Extracted text...",
    "score": 0.95
}
```

#### Stage 2: Summarizer Agent ✍️

```python
Input: { research_results: [...] }
↓
1. Process each source individually
2. Create concise summaries using GPT-4
3. Combine summaries into synthesis
↓
Output: { summaries: [...], combined_summary: "..." }
```

**What it does:**
- Condenses each source to ~150 words
- Uses OpenAI GPT-4 for summarization
- Creates cohesive synthesis of all sources
- Identifies main themes and insights

**OpenAI call:**
```python
response = await openai.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[
        {"role": "system", "content": "You are an expert summarizer"},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)
```

#### Stage 3: Validator Agent ✅

```python
Input: { combined_summary: "..." }
↓
1. Extract 5 key factual claims
2. Validate each claim via web search
3. Assign confidence scores
↓
Output: { validations: [...], overall_confidence: 0.85 }
```

**What it does:**
- Extracts factual claims using GPT-4
- Searches for verification evidence
- Cross-checks each claim
- Assigns confidence (0.0 to 1.0)

**Validation result:**
```python
{
    "claim": "LangGraph enables agent orchestration",
    "verdict": "SUPPORTED",
    "confidence": 0.92,
    "explanation": "Verified across 3 sources",
    "sources": ["url1", "url2", "url3"]
}
```

#### Stage 4: Presenter Agent 💬

```python
Input: { combined_summary, validations, ... }
↓
1. Structure findings with GPT-4
2. Format as markdown
3. Stream response to user
4. Add metadata footer
↓
Output: Streamed markdown response
```

**What it does:**
- Organizes information logically
- Formats with markdown (headings, lists, bold)
- Streams response chunk-by-chunk
- Includes confidence and source metrics

### 4. Response Streaming

```
Presenter → SSE Events → Frontend → UI Update
```

**SSE Events:**
```javascript
// Status update
{
  event: "status",
  data: { stage: "presenting", message: "..." }
}

// Response chunk
{
  event: "response",
  data: { chunk: "## Key Findings\n\n" }
}

// Completion
{
  event: "complete",
  data: { confidence: 0.85, sources_count: 8 }
}
```

**Frontend rendering:**
- Accumulates chunks
- Updates message in real-time
- Renders markdown progressively
- Shows metadata on completion

### 5. Memory Storage

```
Final Response → Weaviate → Vector Embedding
```

**What happens:**
- Final response stored in Weaviate
- OpenAI creates embedding
- Indexed for future semantic search
- Used in future queries for context

## 🧩 Component Details

### Backend Components

#### main.py - FastAPI Application

**Responsibilities:**
- HTTP endpoint management
- Request validation
- Task lifecycle management
- SSE connection handling
- CORS configuration

**Key endpoints:**
```python
GET  /health              # Health check
POST /query               # Create research task
GET  /stream/{task_id}    # SSE stream
GET  /task/{task_id}      # Task status
GET  /tasks               # List all tasks
DELETE /task/{task_id}    # Delete task
```

#### workflows/research_graph.py - LangGraph Orchestration

**Responsibilities:**
- Workflow definition
- State management
- Node transitions
- Error handling
- Stream coordination

**State schema:**
```python
class ResearchState(TypedDict):
    query: str
    research_results: list
    summaries: list
    combined_summary: str
    validations: list
    overall_confidence: float
    final_response: str
    agent_logs: list
    error: str
```

**Graph structure:**
```python
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

#### agents/* - AI Agents

**Common interface:**
```python
class Agent:
    async def execute(self, state: Dict) -> Dict:
        # Process state
        # Call external APIs
        # Update state
        return updated_state
```

#### utils/* - Utility Modules

**weaviate_client.py:**
- Vector database connection
- Schema management
- Embedding storage/retrieval
- Similarity search

**web_search.py:**
- Tavily API wrapper
- Search result processing
- Ranking and filtering
- Mock fallback

**summarization.py:**
- OpenAI integration
- Text summarization
- Summary combination
- Prompt engineering

**validation.py:**
- Claim extraction
- Fact verification
- Confidence scoring
- Multi-source validation

### Frontend Components

#### App.jsx - Root Component

**Responsibilities:**
- Health check on mount
- Error boundary
- Service status display
- Component composition

#### components/ChatUI.jsx - Main Interface

**Responsibilities:**
- Message state management
- SSE connection handling
- User input processing
- Example queries
- Error handling

**State management:**
```javascript
const [messages, setMessages] = useState([]);
const [input, setInput] = useState('');
const [isLoading, setIsLoading] = useState(false);
const [currentStage, setCurrentStage] = useState('');
```

**SSE handling:**
```javascript
const eventSource = new EventSource(streamUrl);

eventSource.addEventListener('response', (event) => {
  const data = JSON.parse(event.data);
  // Accumulate and render chunks
});

eventSource.addEventListener('complete', (event) => {
  // Finalize and cleanup
});
```

#### components/MessageBubble.jsx - Message Display

**Responsibilities:**
- Message rendering
- Markdown formatting
- Metadata display
- Role-based styling

**Message types:**
- User: Blue bubble, right-aligned
- Assistant: White bubble, left-aligned with markdown
- System: Amber bubble, status updates

#### api.js - API Client

**Responsibilities:**
- Axios configuration
- API endpoint abstraction
- Error handling
- URL management

## 🔐 Security Considerations

### API Key Management
- Stored in environment variables
- Never exposed to frontend
- Validated on startup
- Rotation supported

### CORS Policy
- Configurable origins
- Credentials support
- Preflight handling
- Production restrictions

### Input Validation
- Query length limits
- Content sanitization
- Rate limiting (future)
- SQL injection prevention (N/A)

### Error Handling
- Graceful degradation
- User-friendly messages
- Detailed logging
- No sensitive data exposure

## ⚡ Performance Optimizations

### Backend
- Async/await throughout
- Connection pooling
- Response streaming
- Caching (future)

### Frontend
- Vite for fast builds
- Code splitting
- Lazy loading
- Optimistic updates

### Database
- Vector indexing in Weaviate
- Semantic caching
- Batch operations
- Connection reuse

## 📈 Scalability

### Horizontal Scaling
- Stateless backend
- Load balancer ready
- Shared Weaviate instance
- Session storage (future)

### Vertical Scaling
- Configurable worker threads
- Memory optimization
- Batch processing
- Queue system (future)

## 🔍 Monitoring & Observability

### Logging
- Structured logging
- Log levels (DEBUG, INFO, ERROR)
- Agent activity tracking
- Performance metrics

### Health Checks
- Service availability
- API connectivity
- Database status
- Resource usage

### Metrics (Future)
- Request latency
- Success/error rates
- Token usage
- Cache hit rates

## 🧪 Testing Strategy

### Unit Tests
- Agent logic
- Utility functions
- API endpoints
- Component rendering

### Integration Tests
- Workflow execution
- API integration
- Database operations
- SSE streaming

### End-to-End Tests
- Complete user flow
- Browser automation
- Multi-agent coordination
- Error scenarios

## 🔄 Data Flow Diagram

```
┌──────────┐
│   User   │
└────┬─────┘
     │ 1. Submit Query
     ▼
┌──────────────────┐
│   Frontend UI    │
└────┬─────────────┘
     │ 2. POST /query
     ▼
┌──────────────────┐
│  FastAPI Server  │
└────┬─────────────┘
     │ 3. Initialize State
     ▼
┌──────────────────┐
│    LangGraph     │
└────┬─────────────┘
     │ 4. Execute Pipeline
     ▼
┌──────────────────┐  5. Search Web   ┌──────────┐
│   Researcher     │─────────────────▶│  Tavily  │
└────┬─────────────┘                  └──────────┘
     │ 6. Search Memory  ┌──────────┐
     └──────────────────▶│ Weaviate │
     │                   └──────────┘
     ▼
┌──────────────────┐  7. Summarize    ┌──────────┐
│   Summarizer     │─────────────────▶│  OpenAI  │
└────┬─────────────┘                  └──────────┘
     │
     ▼
┌──────────────────┐  8. Validate     ┌──────────┐
│    Validator     │─────────────────▶│  OpenAI  │
└────┬─────────────┘                  └──────────┘
     │
     ▼
┌──────────────────┐  9. Format       ┌──────────┐
│    Presenter     │─────────────────▶│  OpenAI  │
└────┬─────────────┘                  └──────────┘
     │ 10. Stream Response
     ▼
┌──────────────────┐
│   Frontend UI    │
└────┬─────────────┘
     │ 11. Render Markdown
     ▼
┌──────────┐
│   User   │
└──────────┘
```

## 🎯 Design Principles

1. **Modularity**: Each agent is independent and reusable
2. **Extensibility**: Easy to add new agents or modify existing ones
3. **Reliability**: Graceful error handling and fallbacks
4. **Performance**: Async operations and streaming
5. **User Experience**: Real-time feedback and beautiful UI
6. **Maintainability**: Clear structure and documentation

## 📚 Technology Choices

### Why LangGraph?
- Explicit workflow control
- State management
- Debugging capabilities
- Production-ready

### Why FastAPI?
- High performance
- Async support
- Automatic OpenAPI docs
- Type validation

### Why Weaviate?
- Vector storage
- Semantic search
- OpenAI integration
- Scalable

### Why React + Vite?
- Fast development
- Modern tooling
- Great ecosystem
- Easy deployment

---

**For more details on specific components, see the code comments and docstrings.**

