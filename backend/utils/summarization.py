import os
import logging
from typing import List, Dict
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)


class Summarizer:
    """OpenAI-based text summarization utility"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"  # Free model
    
    async def summarize_text(
        self,
        text: str,
        max_length: int = 200,
        style: str = "concise"
    ) -> str:
        """
        Summarize a piece of text
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary in words
            style: "concise", "detailed", or "bullet_points"
        
        Returns:
            Summarized text
        """
        try:
            prompt = self._build_prompt(text, max_length, style)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at summarizing information clearly and accurately."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            summary = response.choices[0].message.content.strip()
            logger.info(f"Summarized text from {len(text)} to {len(summary)} characters")
            return summary
            
        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            # Mock summary when API fails
            words = text.split()[:max_length]
            summary = " ".join(words)
            if len(words) == max_length:
                summary += "..."
            return f"📝 Summary: {summary}"
    
    async def combine_summaries(
        self,
        summaries: List[str],
        query: str
    ) -> str:
        """
        Combine multiple summaries into a cohesive response
        
        Args:
            summaries: List of summary texts
            query: Original user query for context
        
        Returns:
            Combined summary
        """
        try:
            combined_text = "\n\n".join(f"Source {i+1}: {s}" for i, s in enumerate(summaries))
            
            prompt = f"""Given the following summaries from multiple sources about "{query}", 
create a cohesive, well-structured summary that synthesizes the key information.

Summaries:
{combined_text}

Please provide a comprehensive summary that:
1. Identifies the main themes
2. Highlights key insights
3. Notes any contradictions or disagreements
4. Organizes information logically
"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert research analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=800
            )
            
            combined = response.choices[0].message.content.strip()
            logger.info("Combined summaries successfully")
            return combined
            
        except Exception as e:
            logger.error(f"Error combining summaries: {e}")
            return "\n\n".join(summaries)
    
    def _build_prompt(self, text: str, max_length: int, style: str) -> str:
        """Build summarization prompt based on style"""
        style_instructions = {
            "concise": f"Provide a concise summary in approximately {max_length} words.",
            "detailed": f"Provide a detailed summary in approximately {max_length} words.",
            "bullet_points": f"Provide a summary as bullet points (maximum {max_length} words total)."
        }
        
        instruction = style_instructions.get(style, style_instructions["concise"])
        
        return f"""{instruction}

Text to summarize:
{text}

Summary:"""


# Global instance
summarizer = Summarizer()

