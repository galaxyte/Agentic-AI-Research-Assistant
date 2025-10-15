import logging
from typing import Dict, List, Any, AsyncGenerator
from datetime import datetime
from openai import AsyncOpenAI
import os
import json

logger = logging.getLogger(__name__)


class PresenterAgent:
    """Agent responsible for structuring and presenting the final answer"""
    
    def __init__(self):
        self.name = "Presenter"
        self.role = "Communication Specialist"
        self.goal = "Present research findings in a clear, engaging format"
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"  # Free model
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute presentation task
        
        Args:
            state: Current workflow state
        
        Returns:
            Updated state with final presentation
        """
        query = state.get("query", "")
        combined_summary = state.get("combined_summary", "")
        validations = state.get("validations", [])
        overall_confidence = state.get("overall_confidence", 0.5)
        summaries = state.get("summaries", [])
        
        logger.info(f"💬 Presenter crafting final response...")
        
        try:
            # Build the final presentation
            presentation = await self._create_presentation(
                query=query,
                summary=combined_summary,
                validations=validations,
                confidence=overall_confidence,
                summaries=summaries
            )
            
            logger.info(f"✅ Presenter completed final response")
            
            # Update state
            updated_state = {
                **state,
                "final_response": presentation,
                "agent_logs": state.get("agent_logs", []) + [{
                    "agent": self.name,
                    "status": "completed",
                    "message": "Final response prepared",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "response_length": len(presentation)
                    }
                }]
            }
            
            return updated_state
            
        except Exception as e:
            logger.error(f"Error in Presenter: {e}")
            return {
                **state,
                "error": str(e),
                "final_response": combined_summary or "Unable to generate response.",
                "agent_logs": state.get("agent_logs", []) + [{
                    "agent": self.name,
                    "status": "error",
                    "message": f"Error: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }]
            }
    
    async def _create_presentation(
        self,
        query: str,
        summary: str,
        validations: List[Dict],
        confidence: float,
        summaries: List[Dict]
    ) -> str:
        """Create a well-structured presentation of findings"""
        
        # Build context about validations
        validation_context = ""
        if validations:
            validation_context = "\n\nValidation Results:\n"
            for v in validations:
                validation_context += f"- {v['claim']}: {v['verdict']} (confidence: {v['confidence']:.2f})\n"
        
        # Build context about sources
        sources_context = ""
        if summaries:
            sources_context = "\n\nSources:\n"
            for idx, s in enumerate(summaries[:5], 1):
                sources_context += f"{idx}. {s['source_title']}\n"
        
        prompt = f"""You are presenting research findings to a user. Create a comprehensive, well-structured response.

User Query: {query}

Research Summary:
{summary}
{validation_context}
{sources_context}

Overall Confidence Score: {confidence:.2f}

Please create a final response that:
1. Directly answers the user's query
2. Presents key findings in a clear, organized manner
3. Uses markdown formatting (headings, bullet points, bold, etc.)
4. Includes the confidence assessment
5. Cites the number of sources verified
6. Is engaging and easy to read

Format the response professionally with proper markdown."""

        try:
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert research presenter who communicates complex information clearly."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.6,
                    max_tokens=1200
                )
            except Exception as api_error:
                logger.error(f"API error in presentation: {api_error}")
                # Mock presentation when API fails
                return self._create_basic_presentation(query, summary, summaries, confidence)
            
            presentation = response.choices[0].message.content.strip()
            
            # Add metadata footer
            sources_count = len(summaries)
            claims_validated = len(validations)
            
            footer = f"\n\n---\n\n**Research Metadata:**\n"
            footer += f"- 📚 Sources analyzed: {sources_count}\n"
            footer += f"- ✅ Claims validated: {claims_validated}\n"
            footer += f"- 🎯 Overall confidence: {confidence:.1%}\n"
            
            return presentation + footer
            
        except Exception as e:
            logger.error(f"Error creating presentation: {e}")
            # Fallback to basic presentation
            return self._create_basic_presentation(query, summary, summaries, confidence)
    
    def _create_basic_presentation(
        self,
        query: str,
        summary: str,
        summaries: List[Dict],
        confidence: float
    ) -> str:
        """Create a basic presentation without AI enhancement"""
        
        presentation = f"# Research Results: {query}\n\n"
        presentation += f"## Summary\n\n{summary}\n\n"
        
        if summaries:
            presentation += "## Sources\n\n"
            for idx, s in enumerate(summaries[:5], 1):
                presentation += f"{idx}. **{s['source_title']}**\n"
                presentation += f"   {s['summary'][:200]}...\n\n"
        
        presentation += f"\n**Confidence Level:** {confidence:.1%}\n"
        presentation += f"**Sources Analyzed:** {len(summaries)}\n"
        
        return presentation
    
    async def stream_presentation(
        self,
        state: Dict[str, Any]
    ) -> AsyncGenerator[str, None]:
        """
        Stream the presentation in chunks
        
        Yields:
            Chunks of the presentation
        """
        query = state.get("query", "")
        combined_summary = state.get("combined_summary", "")
        validations = state.get("validations", [])
        overall_confidence = state.get("overall_confidence", 0.5)
        summaries = state.get("summaries", [])
        
        try:
            # Build validation context
            validation_context = ""
            if validations:
                validation_context = "\n\nValidation Results:\n"
                for v in validations:
                    validation_context += f"- {v['claim']}: {v['verdict']} (confidence: {v['confidence']:.2f})\n"
            
            # Build sources context
            sources_context = ""
            if summaries:
                sources_context = "\n\nSources:\n"
                for idx, s in enumerate(summaries[:5], 1):
                    sources_context += f"{idx}. {s['source_title']}\n"
            
            prompt = f"""You are presenting research findings to a user. Create a comprehensive, well-structured response.

User Query: {query}

Research Summary:
{combined_summary}
{validation_context}
{sources_context}

Overall Confidence Score: {overall_confidence:.2f}

Please create a final response that:
1. Directly answers the user's query
2. Presents key findings in a clear, organized manner
3. Uses markdown formatting (headings, bullet points, bold, etc.)
4. Includes the confidence assessment
5. Cites the number of sources verified
6. Is engaging and easy to read

Format the response professionally with proper markdown."""

            # Stream the response
            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert research presenter who communicates complex information clearly."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=1200,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
            
            # Add metadata footer
            sources_count = len(summaries)
            claims_validated = len(validations)
            
            footer = f"\n\n---\n\n**Research Metadata:**\n"
            footer += f"- 📚 Sources analyzed: {sources_count}\n"
            footer += f"- ✅ Claims validated: {claims_validated}\n"
            footer += f"- 🎯 Overall confidence: {overall_confidence:.1%}\n"
            
            yield footer
            
        except Exception as e:
            logger.error(f"Error streaming presentation: {e}")
            yield f"\n\nError creating presentation: {str(e)}\n\n"
            yield combined_summary or "Unable to generate response."


# Global instance
presenter_agent = PresenterAgent()

