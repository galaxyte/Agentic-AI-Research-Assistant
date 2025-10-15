import os
import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.query import MetadataQuery
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class WeaviateMemory:
    """Weaviate client for semantic memory storage and retrieval"""
    
    def __init__(self):
        self.url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
        self.api_key = os.getenv("WEAVIATE_API_KEY")
        self.client = None
        self.collection_name = "ResearchSnippet"
        
    async def connect(self):
        """Initialize connection to Weaviate"""
        try:
            if self.api_key:
                self.client = weaviate.connect_to_custom(
                    http_host=self.url.replace("http://", "").replace("https://", ""),
                    http_port=8080,
                    http_secure=False,
                    auth_credentials=weaviate.auth.AuthApiKey(self.api_key)
                )
            else:
                self.client = weaviate.connect_to_local(
                    host=self.url.replace("http://", "").replace("https://", "").split(":")[0],
                    port=8080
                )
            
            await self._create_schema()
            logger.info("Connected to Weaviate successfully")
        except Exception as e:
            logger.warning(f"Weaviate connection failed: {e}. Continuing without vector memory.")
            self.client = None
    
    async def _create_schema(self):
        """Create Weaviate schema if it doesn't exist"""
        if not self.client:
            return
            
        try:
            # Check if collection exists
            if not self.client.collections.exists(self.collection_name):
                self.client.collections.create(
                    name=self.collection_name,
                    vectorizer_config=Configure.Vectorizer.text2vec_openai(
                        model="text-embedding-3-small"
                    ),
                    properties=[
                        Property(name="query", data_type=DataType.TEXT),
                        Property(name="content", data_type=DataType.TEXT),
                        Property(name="source", data_type=DataType.TEXT),
                        Property(name="validation_score", data_type=DataType.NUMBER),
                        Property(name="timestamp", data_type=DataType.TEXT),
                    ]
                )
                logger.info(f"Created collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error creating schema: {e}")
    
    async def store_snippet(
        self,
        query: str,
        content: str,
        source: str,
        validation_score: float = 0.0,
        timestamp: str = ""
    ):
        """Store a research snippet in Weaviate"""
        if not self.client:
            logger.warning("Weaviate not connected, skipping storage")
            return
        
        try:
            collection = self.client.collections.get(self.collection_name)
            collection.data.insert(
                properties={
                    "query": query,
                    "content": content,
                    "source": source,
                    "validation_score": validation_score,
                    "timestamp": timestamp
                }
            )
            logger.info(f"Stored snippet for query: {query[:50]}...")
        except Exception as e:
            logger.error(f"Error storing snippet: {e}")
    
    async def search_similar(
        self,
        query: str,
        limit: int = 5
    ) -> List[Dict]:
        """Search for similar research snippets"""
        if not self.client:
            logger.warning("Weaviate not connected, returning empty results")
            return []
        
        try:
            collection = self.client.collections.get(self.collection_name)
            response = collection.query.near_text(
                query=query,
                limit=limit,
                return_metadata=MetadataQuery(distance=True)
            )
            
            results = []
            for obj in response.objects:
                results.append({
                    "content": obj.properties.get("content", ""),
                    "source": obj.properties.get("source", ""),
                    "validation_score": obj.properties.get("validation_score", 0.0),
                    "distance": obj.metadata.distance if obj.metadata else 1.0
                })
            
            logger.info(f"Found {len(results)} similar snippets")
            return results
        except Exception as e:
            logger.error(f"Error searching snippets: {e}")
            return []
    
    async def close(self):
        """Close Weaviate connection"""
        if self.client:
            self.client.close()
            logger.info("Weaviate connection closed")


# Global instance
weaviate_memory = WeaviateMemory()

