"""
The Revelation Engine: transforms raw data into profound narrative insights.
"""

import logging
import hashlib
import json
from typing import Dict, Any, Optional
import openai
from brain import Brain

logger = logging.getLogger(__name__)

class RevelationEngine:
    def __init__(self, brain: Brain, openai_api_key: str):
        self.brain = brain
        openai.api_key = openai_api_key

    def generate_insight(self, client_id: str, data_sources: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an insight from the given data sources.
        Returns a dictionary with the insight and metadata.
        """
        # Combine and hash the data sources for caching
        data_hash = hashlib.md5(json.dumps(data_sources, sort_keys=True).encode()).hexdigest()

        # Check if we have a recent cached insight for this data hash
        cached_insight = self._get_cached_insight(client_id, data_hash)
        if cached_insight:
            logger.info(f"Using cached insight for client {client_id}")
            return cached_insight

        # Otherwise, generate a new insight
        try:
            # Prepare the prompt for OpenAI
            prompt = self._build_prompt(data_sources)
            response = openai.ChatCompletion.create(
                model="gpt-4",  # or "gpt-3.5-turbo" for cost savings
                messages=[
                    {"role": "system", "content": "You are a strategic business analyst. Your task is to provide a single, profound narrative insight from the provided data. The insight should be actionable and surprising."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            insight_text = response.choices[0].message.content.strip()

            # Build the insight object
            insight = {
                "insight_text": insight_text,
                "data_sources_hash": data_hash,
                "confidence_score": self._calculate_confidence(insight_text, data_sources),
                "suggested_actions": self._generate_suggested_actions(insight_text),
                "timestamp": None  # to be set by brain.store_insight
            }

            # Store the insight in the brain
            self.brain.store_insight(client_id, insight)

            # Log the generation
            self.brain.log_system_health({
                "event": "insight_generated",
                "client_id": client_id,
                "data_hash": data_hash,
                "openai_usage": response.usage.to_dict() if hasattr(response, 'usage') else None
            })

            return insight

        except Exception as e:
            logger.error(f"Error generating insight: {e}")
            # Fallback: return the last insight from the brain
            last_insight = self.brain.get_latest_insight(client_id)
            if last_insight:
                logger.info("Falling back to last insight")
                return last_insight
            else:
                # If no last insight, return a default
                return {
                    "insight_text": "We are currently unable to generate an insight. Please try again later.",
                    "data_sources_hash": None,
                    "confidence_score": 0.0,
                    "suggested_actions": [],
                    "timestamp": None
                }

    def _build_prompt(self, data_sources: Dict[str, Any]) -> str:
        """Build a prompt for OpenAI from the data sources."""
        # This is a simple example. In practice, we would format the data sources appropriately.
        prompt = f"""
        Given the following data from a SaaS company, provide one profound narrative insight that could help them understand user behavior or improve conversion:

        Data:
        {json.dumps(data_sources, indent=2)}

        Insight:
        """
        return prompt

    def _calculate_confidence(self, insight_text: str, data_sources: Dict[str, Any]) -> float:
        """Calculate a confidence score for the insight (placeholder)."""
        # This is a placeholder. In a real system, we might use a model to score the insight.
        # For now, return a default high score.
        return 0.9

    def _generate_suggested_actions(self, insight_text: str) -> list:
        """Generate suggested actions from the insight (placeholder)."""
        # This is a placeholder. In a real system, we might use another LLM call to generate actions.
        return ["Review the insight and consider adjusting your product roadmap."]

    def _get_cached_insight(self, client_id: str, data_hash: str) -> Optional[Dict[str, Any]]:
        """Check if we have a cached insight for this data hash (within the last 24 hours)."""
        # We can implement a caching mechanism here. For now, we return None to always generate new.
        return None