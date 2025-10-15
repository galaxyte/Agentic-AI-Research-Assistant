import logging
from typing import Dict, List, Any
from datetime import datetime
from utils.summarization import summarizer

logger = logging.getLogger(__name__)


class SummarizerAgent:
    """Agent responsible for condensing research into clean insights"""
    
    def __init__(self):
        self.name = "Summarizer"
        self.role = "Information Synthesis Specialist"
        self.goal = "Condense complex information into clear, actionable insights"
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute summarization task
        
        Args:
            state: Current workflow state containing 'research_results'
        
        Returns:
            Updated state with summaries
        """
        query = state.get("query", "")
        research_results = state.get("research_results", [])
        
        logger.info(f"✍️ Summarizer processing {len(research_results)} sources...")
        
        try:
            if not research_results:
                logger.warning("No research results to summarize")
                return {
                    **state,
                    "summaries": [],
                    "agent_logs": state.get("agent_logs", []) + [{
                        "agent": self.name,
                        "status": "skipped",
                        "message": "No research results to summarize",
                        "timestamp": datetime.now().isoformat()
                    }]
                }
            
            # Summarize each source
            summaries = []
            for idx, result in enumerate(research_results[:8]):  # Limit to top 8
                try:
                    content = result.get("content", "")
                    if len(content) < 100:  # Skip very short content
                        continue
                    
                    summary = await summarizer.summarize_text(
                        text=content,
                        max_length=150,
                        style="concise"
                    )
                    
                    summaries.append({
                        "source_title": result.get("title", f"Source {idx + 1}"),
                        "source_url": result.get("url", ""),
                        "summary": summary,
                        "original_score": result.get("score", 0.0)
                    })
                    
                except Exception as e:
                    logger.error(f"Error summarizing result {idx}: {e}")
                    continue
            
            # Create a combined synthesis
            if summaries:
                summary_texts = [s["summary"] for s in summaries]
                combined_summary = await summarizer.combine_summaries(
                    summaries=summary_texts,
                    query=query
                )
            else:
                combined_summary = "Unable to generate summary from available sources."
            
            logger.info(f"✅ Summarizer created {len(summaries)} summaries")
            
            # Update state
            updated_state = {
                **state,
                "summaries": summaries,
                "combined_summary": combined_summary,
                "agent_logs": state.get("agent_logs", []) + [{
                    "agent": self.name,
                    "status": "completed",
                    "message": f"Created {len(summaries)} summaries and synthesis",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "summary_count": len(summaries),
                        "synthesis_length": len(combined_summary)
                    }
                }]
            }
            
            return updated_state
            
        except Exception as e:
            logger.error(f"Error in Summarizer: {e}")
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
summarizer_agent = SummarizerAgent()

