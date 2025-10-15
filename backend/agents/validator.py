import logging
from typing import Dict, List, Any
from datetime import datetime
from utils.validation import fact_validator

logger = logging.getLogger(__name__)


class ValidatorAgent:
    """Agent responsible for validating facts and assigning confidence scores"""
    
    def __init__(self):
        self.name = "Validator"
        self.role = "Fact Verification Specialist"
        self.goal = "Verify accuracy and reliability of information"
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute validation task
        
        Args:
            state: Current workflow state containing 'combined_summary'
        
        Returns:
            Updated state with validation results
        """
        combined_summary = state.get("combined_summary", "")
        summaries = state.get("summaries", [])
        
        logger.info(f"✅ Validator checking facts...")
        
        try:
            if not combined_summary:
                logger.warning("No summary to validate")
                return {
                    **state,
                    "validations": [],
                    "overall_confidence": 0.0,
                    "agent_logs": state.get("agent_logs", []) + [{
                        "agent": self.name,
                        "status": "skipped",
                        "message": "No summary to validate",
                        "timestamp": datetime.now().isoformat()
                    }]
                }
            
            # Extract and validate key claims
            validations = await fact_validator.extract_and_validate_claims(
                text=combined_summary,
                max_claims=5
            )
            
            # Calculate overall confidence
            if validations:
                confidence_scores = [v["confidence"] for v in validations]
                overall_confidence = sum(confidence_scores) / len(confidence_scores)
                
                # Count verdicts
                verdicts = [v["verdict"] for v in validations]
                supported_count = verdicts.count("SUPPORTED")
                contradicted_count = verdicts.count("CONTRADICTED")
            else:
                overall_confidence = 0.5
                supported_count = 0
                contradicted_count = 0
            
            logger.info(f"✅ Validator completed: {len(validations)} claims checked")
            logger.info(f"   Overall confidence: {overall_confidence:.2f}")
            logger.info(f"   Supported: {supported_count}, Contradicted: {contradicted_count}")
            
            # Update state
            updated_state = {
                **state,
                "validations": validations,
                "overall_confidence": overall_confidence,
                "validation_stats": {
                    "total_claims": len(validations),
                    "supported": supported_count,
                    "contradicted": contradicted_count,
                    "confidence": overall_confidence
                },
                "agent_logs": state.get("agent_logs", []) + [{
                    "agent": self.name,
                    "status": "completed",
                    "message": f"Validated {len(validations)} claims (confidence: {overall_confidence:.2f})",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "claims_validated": len(validations),
                        "overall_confidence": overall_confidence,
                        "supported_claims": supported_count,
                        "contradicted_claims": contradicted_count
                    }
                }]
            }
            
            return updated_state
            
        except Exception as e:
            logger.error(f"Error in Validator: {e}")
            return {
                **state,
                "error": str(e),
                "validations": [],
                "overall_confidence": 0.5,
                "agent_logs": state.get("agent_logs", []) + [{
                    "agent": self.name,
                    "status": "error",
                    "message": f"Error: {str(e)}",
                    "timestamp": datetime.now().isoformat()
                }]
            }


# Global instance
validator_agent = ValidatorAgent()

