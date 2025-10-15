import os
import logging
import asyncio
import json
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any

from dotenv import load_dotenv

# Load environment variables FIRST before other imports
load_dotenv()

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from workflows.research_graph import research_workflow
from agents.presenter import presenter_agent
from utils.weaviate_client import weaviate_memory
from utils.web_search import web_searcher
from utils.summarization import summarizer
from utils.validation import fact_validator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Task storage
active_tasks: Dict[str, Dict[str, Any]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown"""
    # Startup
    logger.info("🚀 Starting Agentic AI Research Assistant...")
    
    # Initialize Weaviate
    try:
        await weaviate_memory.connect()
        logger.info("✅ Weaviate connected")
    except Exception as e:
        logger.warning(f"⚠️ Weaviate connection failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down...")
    await weaviate_memory.close()


app = FastAPI(
    title="Agentic AI Research Assistant",
    description="Multi-agent AI system for autonomous research and analysis",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class QueryRequest(BaseModel):
    query: str
    stream: bool = True


class QueryResponse(BaseModel):
    task_id: str
    status: str
    message: str


class TaskStatus(BaseModel):
    task_id: str
    status: str
    current_stage: str
    final_response: str = ""
    error: str = ""


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "operational",
        "service": "Agentic AI Research Assistant",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "weaviate": "connected" if weaviate_memory.client else "disconnected",
        "openai": "configured" if os.getenv("OPENAI_API_KEY") else "not configured",
        "tavily": "configured" if os.getenv("TAVILY_API_KEY") else "not configured",
        "active_tasks": len(active_tasks)
    }


@app.post("/query", response_model=QueryResponse)
async def create_query(request: QueryRequest, background_tasks: BackgroundTasks):
    """
    Create a new research query
    
    Args:
        request: Query request with query text and streaming preference
    
    Returns:
        Task ID and status
    """
    if not request.query or len(request.query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Generate task ID
    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    
    # Initialize task
    active_tasks[task_id] = {
        "status": "initializing",
        "query": request.query,
        "current_stage": "Starting...",
        "final_response": "",
        "error": "",
        "created_at": datetime.now().isoformat()
    }
    
    # Start background task if not streaming
    if not request.stream:
        background_tasks.add_task(execute_research_task, task_id, request.query)
    
    logger.info(f"📝 Created task {task_id}: {request.query[:50]}...")
    
    return QueryResponse(
        task_id=task_id,
        status="created",
        message="Research task created successfully"
    )


async def execute_research_task(task_id: str, query: str):
    """Execute research workflow in background"""
    try:
        active_tasks[task_id]["status"] = "running"
        
        # Run workflow
        final_state = await research_workflow.run(query)
        
        # Store in memory
        if final_state.get("final_response"):
            await weaviate_memory.store_snippet(
                query=query,
                content=final_state["final_response"],
                source="research_workflow",
                validation_score=final_state.get("overall_confidence", 0.0),
                timestamp=datetime.now().isoformat()
            )
        
        # Update task
        active_tasks[task_id].update({
            "status": "completed",
            "current_stage": "Completed",
            "final_response": final_state.get("final_response", ""),
            "error": final_state.get("error", ""),
            "completed_at": datetime.now().isoformat()
        })
        
        logger.info(f"✅ Task {task_id} completed")
        
    except Exception as e:
        logger.error(f"❌ Task {task_id} failed: {e}")
        active_tasks[task_id].update({
            "status": "failed",
            "error": str(e),
            "completed_at": datetime.now().isoformat()
        })


@app.get("/task/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str):
    """Get status of a research task"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = active_tasks[task_id]
    return TaskStatus(
        task_id=task_id,
        status=task["status"],
        current_stage=task["current_stage"],
        final_response=task.get("final_response", ""),
        error=task.get("error", "")
    )


@app.get("/stream/{task_id}")
async def stream_research(task_id: str):
    """
    Stream research progress and results using Server-Sent Events
    
    Args:
        task_id: Task identifier
    
    Returns:
        SSE stream of research progress
    """
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = active_tasks[task_id]
    query = task["query"]
    
    async def event_generator():
        try:
            # Send initial status
            yield {
                "event": "status",
                "data": json.dumps({
                    "stage": "initializing",
                    "message": "Starting research workflow..."
                })
            }
            
            # Stream workflow progress
            async for state_update in research_workflow.stream_run(query):
                # Extract the actual state from the update
                # LangGraph yields {node_name: state}
                for node_name, state in state_update.items():
                    if isinstance(state, dict):
                        # Send stage update
                        current_stage = state.get("current_stage", node_name)
                        yield {
                            "event": "stage",
                            "data": json.dumps({
                                "stage": node_name,
                                "message": current_stage,
                                "timestamp": datetime.now().isoformat()
                            })
                        }
                        
                        # Send agent logs if available
                        agent_logs = state.get("agent_logs", [])
                        if agent_logs:
                            latest_log = agent_logs[-1]
                            yield {
                                "event": "log",
                                "data": json.dumps(latest_log)
                            }
                        
                        # Update task status
                        active_tasks[task_id].update({
                            "status": "running",
                            "current_stage": current_stage
                        })
            
            # Get final state
            final_state = await research_workflow.run(query)
            
            # Stream final response
            yield {
                "event": "status",
                "data": json.dumps({
                    "stage": "presenting",
                    "message": "Streaming final response..."
                })
            }
            
            # Stream the presentation
            async for chunk in presenter_agent.stream_presentation(final_state):
                yield {
                    "event": "response",
                    "data": json.dumps({"chunk": chunk})
                }
            
            # Store in memory
            if final_state.get("final_response"):
                await weaviate_memory.store_snippet(
                    query=query,
                    content=final_state["final_response"],
                    source="research_workflow",
                    validation_score=final_state.get("overall_confidence", 0.0),
                    timestamp=datetime.now().isoformat()
                )
            
            # Update task
            active_tasks[task_id].update({
                "status": "completed",
                "current_stage": "Completed",
                "final_response": final_state.get("final_response", ""),
                "completed_at": datetime.now().isoformat()
            })
            
            # Send completion event
            yield {
                "event": "complete",
                "data": json.dumps({
                    "message": "Research completed",
                    "confidence": final_state.get("overall_confidence", 0.0),
                    "sources_count": len(final_state.get("summaries", []))
                })
            }
            
            logger.info(f"✅ Streaming completed for task {task_id}")
            
        except Exception as e:
            logger.error(f"❌ Streaming error for task {task_id}: {e}")
            yield {
                "event": "error",
                "data": json.dumps({
                    "error": str(e),
                    "message": "An error occurred during research"
                })
            }
            
            active_tasks[task_id].update({
                "status": "failed",
                "error": str(e)
            })
    
    return EventSourceResponse(event_generator())


@app.delete("/task/{task_id}")
async def delete_task(task_id: str):
    """Delete a completed task"""
    if task_id not in active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del active_tasks[task_id]
    logger.info(f"🗑️ Deleted task {task_id}")
    
    return {"message": "Task deleted successfully"}


@app.get("/tasks")
async def list_tasks():
    """List all tasks"""
    return {
        "tasks": [
            {
                "task_id": task_id,
                "query": task["query"][:100],
                "status": task["status"],
                "created_at": task["created_at"]
            }
            for task_id, task in active_tasks.items()
        ],
        "total": len(active_tasks)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

