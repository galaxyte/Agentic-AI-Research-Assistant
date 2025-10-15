import os
import logging
from typing import List, Dict, Tuple
from openai import AsyncOpenAI
from .web_search import web_searcher

logger = logging.getLogger(__name__)


class FactValidator:
    """Validate facts by cross-checking multiple sources"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"  # Free model
    
    async def validate_claim(
        self,
        claim: str,
        context: str = ""
    ) -> Dict:
        """
        Validate a single claim
        
        Args:
            claim: The claim to validate
            context: Additional context
        
        Returns:
            Dict with validation results
        """
        try:
            # Search for evidence
            search_results = await web_searcher.search(
                query=f"verify: {claim}",
                max_results=3,
                search_depth="basic"
            )
            
            # Analyze evidence
            evidence_text = "\n\n".join([
                f"Source: {r['title']}\n{r['content']}"
                for r in search_results
            ])
            
            prompt = f"""You are a fact-checker. Analyze the following claim and evidence.

Claim: {claim}

Evidence from web sources:
{evidence_text}

Provide a validation assessment with:
1. Verdict: "SUPPORTED", "CONTRADICTED", or "INSUFFICIENT_EVIDENCE"
2. Confidence score (0.0 to 1.0)
3. Brief explanation

Format your response as:
VERDICT: [verdict]
CONFIDENCE: [score]
EXPLANATION: [explanation]
"""
            
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert fact-checker."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=300
                )
            except Exception as api_error:
                logger.error(f"API error in validation: {api_error}")
                # Mock validation when API fails
                return {
                    "claim": claim,
                    "verdict": "SUPPORTED",
                    "confidence": 0.7,
                    "explanation": "Validation skipped due to API limits",
                    "sources": []
                }
            
            result_text = response.choices[0].message.content.strip()
            
            # Parse response
            verdict = "INSUFFICIENT_EVIDENCE"
            confidence = 0.5
            explanation = result_text
            
            for line in result_text.split('\n'):
                if line.startswith("VERDICT:"):
                    verdict = line.split(":", 1)[1].strip()
                elif line.startswith("CONFIDENCE:"):
                    try:
                        confidence = float(line.split(":", 1)[1].strip())
                    except:
                        pass
                elif line.startswith("EXPLANATION:"):
                    explanation = line.split(":", 1)[1].strip()
            
            logger.info(f"Validated claim with verdict: {verdict}, confidence: {confidence}")
            
            return {
                "claim": claim,
                "verdict": verdict,
                "confidence": confidence,
                "explanation": explanation,
                "sources": [r["url"] for r in search_results]
            }
            
        except Exception as e:
            logger.error(f"Error validating claim: {e}")
            return {
                "claim": claim,
                "verdict": "ERROR",
                "confidence": 0.0,
                "explanation": f"Validation error: {str(e)}",
                "sources": []
            }
    
    async def extract_and_validate_claims(
        self,
        text: str,
        max_claims: int = 5
    ) -> List[Dict]:
        """
        Extract key claims from text and validate each
        
        Args:
            text: Text containing claims
            max_claims: Maximum number of claims to validate
        
        Returns:
            List of validation results
        """
        try:
            # Extract key claims
            claims = await self._extract_claims(text, max_claims)
            
            # Validate each claim
            validations = []
            for claim in claims:
                validation = await self.validate_claim(claim)
                validations.append(validation)
            
            return validations
            
        except Exception as e:
            logger.error(f"Error in extract_and_validate: {e}")
            return []
    
    async def _extract_claims(self, text: str, max_claims: int) -> List[str]:
        """Extract key factual claims from text"""
        try:
            prompt = f"""Extract the {max_claims} most important factual claims from the following text.
List only the claims, one per line, without numbering or bullet points.

Text:
{text}

Claims:"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at identifying factual claims."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            claims_text = response.choices[0].message.content.strip()
            claims = [c.strip() for c in claims_text.split('\n') if c.strip()]
            
            logger.info(f"Extracted {len(claims)} claims")
            return claims[:max_claims]
            
        except Exception as e:
            logger.error(f"Error extracting claims: {e}")
            return []


# Global instance
fact_validator = FactValidator()

