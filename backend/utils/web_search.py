import os
import logging
from typing import List, Dict
from tavily import TavilyClient

logger = logging.getLogger(__name__)


class WebSearcher:
    """Web search utility using Tavily API"""
    
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            logger.warning("TAVILY_API_KEY not found. Web search will be limited.")
            self.client = None
        else:
            self.client = TavilyClient(api_key=api_key)
    
    async def search(
        self,
        query: str,
        max_results: int = 5,
        search_depth: str = "advanced"
    ) -> List[Dict[str, str]]:
        """
        Search the web for information
        
        Args:
            query: Search query
            max_results: Maximum number of results
            search_depth: "basic" or "advanced"
        
        Returns:
            List of search results with title, url, and content
        """
        if not self.client:
            logger.warning("Tavily client not initialized")
            return self._get_mock_results(query)
        
        try:
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth=search_depth,
                include_answer=True,
                include_raw_content=False
            )
            
            results = []
            for result in response.get("results", []):
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "score": result.get("score", 0.0)
                })
            
            # Add the answer if available
            if response.get("answer"):
                results.insert(0, {
                    "title": "AI Summary",
                    "url": "tavily://answer",
                    "content": response["answer"],
                    "score": 1.0
                })
            
            logger.info(f"Found {len(results)} results for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"Error during web search: {e}")
            return self._get_mock_results(query)
    
    def _get_mock_results(self, query: str) -> List[Dict[str, str]]:
        """Return mock results when API is unavailable"""
        return [
            {
                "title": f"Mock Result for: {query}",
                "url": "https://example.com",
                "content": f"This is a mock search result for the query: {query}. "
                          "To get real results, please configure TAVILY_API_KEY in your environment.",
                "score": 0.8
            }
        ]


# Global instance
web_searcher = WebSearcher()

