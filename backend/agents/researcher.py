import logging
from typing import Dict, List, Any
from datetime import datetime
from utils.web_search import web_searcher
from utils.weaviate_client import weaviate_memory

logger = logging.getLogger(__name__)


class ResearcherAgent:
    """Agent responsible for searching and gathering information from the web"""
    
    def __init__(self):
        self.name = "Researcher"
        self.role = "Web Research Specialist"
        self.goal = "Find relevant and accurate information from web sources"
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute research task
        
        Args:
            state: Current workflow state containing 'query'
        
        Returns:
            Updated state with research results
        """
        query = state.get("query", "")
        logger.info(f"🧑‍🔬 Researcher starting work on: {query[:50]}...")
        
        try:
            # Check semantic memory for similar past research
            similar_snippets = await weaviate_memory.search_similar(query, limit=3)
            
            memory_context = ""
            if similar_snippets:
                memory_context = "\n\nRelevant past research:\n" + "\n".join([
                    f"- {s['content'][:100]}..." for s in similar_snippets
                ])
                logger.info(f"Found {len(similar_snippets)} relevant past research snippets")
            
            # Perform web search
            search_results = await web_searcher.search(
                query=query,
                max_results=10,
                search_depth="advanced"
            )
            
            if not search_results:
                logger.warning("No search results found")
                return {
                    **state,
                    "research_results": [],
                    "error": "No search results found",
                    "agent_logs": state.get("agent_logs", []) + [{
                        "agent": self.name,
                        "status": "error",
                        "message": "No search results found",
                        "timestamp": datetime.now().isoformat()
                    }]
                }
            
            # Process results
            processed_results = []
            for result in search_results:
                processed_results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "score": result.get("score", 0.0)
                })
            
            logger.info(f"✅ Researcher found {len(processed_results)} relevant sources")
            
            # Update state
            updated_state = {
                **state,
                "research_results": processed_results,
                "memory_context": memory_context,
                "agent_logs": state.get("agent_logs", []) + [{
                    "agent": self.name,
                    "status": "completed",
                    "message": f"Found {len(processed_results)} relevant sources",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "sources_count": len(processed_results),
                        "top_source": processed_results[0]["title"] if processed_results else None
                    }
                }]
            }
            
            return updated_state
            
        except Exception as e:
            logger.error(f"Error in Researcher: {e}")
            return {
                **state,
                "error": str(e),
                "agent_logs": state.get("agent_logs", []) + [{
                    "agent": self.name,
                    "status": "error",
                    "message": f"Error: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }]
            }


# Global instance
researcher_agent = ResearcherAgent()

