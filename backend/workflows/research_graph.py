import logging
from typing import Dict, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from agents.researcher import researcher_agent
from agents.summarizer import summarizer_agent
from agents.validator import validator_agent
from agents.presenter import presenter_agent
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)


class ResearchState(TypedDict):
    """State schema for the research workflow"""
    query: str
    research_results: list
    summaries: list
    combined_summary: str
    validations: list
    overall_confidence: float
    validation_stats: dict
    final_response: str
    memory_context: str
    agent_logs: list
    error: str
    current_stage: str


class ResearchWorkflow:
    """LangGraph-based workflow orchestrating research agents"""
    
    def __init__(self):
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create the state graph
        workflow = StateGraph(ResearchState)
        
        # Add nodes for each agent
        workflow.add_node("researcher", self._researcher_node)
        workflow.add_node("summarizer", self._summarizer_node)
        workflow.add_node("validator", self._validator_node)
        workflow.add_node("presenter", self._presenter_node)
        
        # Define the flow
        workflow.set_entry_point("researcher")
        workflow.add_edge("researcher", "summarizer")
        workflow.add_edge("summarizer", "validator")
        workflow.add_edge("validator", "presenter")
        workflow.add_edge("presenter", END)
        
        # Compile the graph
        return workflow.compile()
    
    async def _researcher_node(self, state: ResearchState) -> ResearchState:
        """Execute researcher agent"""
        logger.info("📍 Stage: Researcher")
        state["current_stage"] = "Researching web sources..."
        result = await researcher_agent.execute(dict(state))
        return result
    
    async def _summarizer_node(self, state: ResearchState) -> ResearchState:
        """Execute summarizer agent"""
        logger.info("📍 Stage: Summarizer")
        state["current_stage"] = "Summarizing findings..."
        result = await summarizer_agent.execute(dict(state))
        return result
    
    async def _validator_node(self, state: ResearchState) -> ResearchState:
        """Execute validator agent"""
        logger.info("📍 Stage: Validator")
        state["current_stage"] = "Validating facts..."
        result = await validator_agent.execute(dict(state))
        return result
    
    async def _presenter_node(self, state: ResearchState) -> ResearchState:
        """Execute presenter agent"""
        logger.info("📍 Stage: Presenter")
        state["current_stage"] = "Preparing final response..."
        result = await presenter_agent.execute(dict(state))
        return result
    
    async def run(self, query: str) -> Dict[str, Any]:
        """
        Run the complete research workflow
        
        Args:
            query: User's research query
        
        Returns:
            Final state with research results
        """
        logger.info(f"🚀 Starting research workflow for: {query[:50]}...")
        
        # Initialize state
        initial_state = {
            "query": query,
            "research_results": [],
            "summaries": [],
            "combined_summary": "",
            "validations": [],
            "overall_confidence": 0.0,
            "validation_stats": {},
            "final_response": "",
            "memory_context": "",
            "agent_logs": [],
            "error": "",
            "current_stage": "Initializing..."
        }
        
        try:
            # Execute the workflow
            final_state = await self.graph.ainvoke(initial_state)
            
            logger.info("✅ Research workflow completed successfully")
            return final_state
            
        except Exception as e:
            logger.error(f"Error in research workflow: {e}")
            return {
                **initial_state,
                "error": str(e),
                "final_response": f"Error during research: {str(e)}"
            }
    
    async def stream_run(self, query: str):
        """
        Run the workflow with streaming updates
        
        Args:
            query: User's research query
        
        Yields:
            State updates at each stage
        """
        logger.info(f"🚀 Starting streaming research workflow for: {query[:50]}...")
        
        # Initialize state
        initial_state = {
            "query": query,
            "research_results": [],
            "summaries": [],
            "combined_summary": "",
            "validations": [],
            "overall_confidence": 0.0,
            "validation_stats": {},
            "final_response": "",
            "memory_context": "",
            "agent_logs": [],
            "error": "",
            "current_stage": "Initializing..."
        }
        
        try:
            # Stream through each node
            async for state in self.graph.astream(initial_state):
                # Yield the current state
                yield state
                
        except Exception as e:
            logger.error(f"Error in streaming workflow: {e}")
            yield {
                "error": {
                    **initial_state,
                    "error": str(e),
                    "final_response": f"Error during research: {str(e)}"
                }
            }


# Global instance
research_workflow = ResearchWorkflow()

