"""
The Persistent Brain for the Magnetic Oracle.
Handles all Firestore interactions and maintains state.
"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from google.cloud import firestore
from google.oauth2 import service_account

logger = logging.getLogger(__name__)

def get_firestore_client(project_id: str) -> firestore.Client:
    """
    Initialize and return a Firestore client.
    Assumes that the GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    Alternatively, we can use a service account key file.
    """
    # If running in production (e.g., Google Cloud), no credentials are needed.
    # Otherwise, we can use a service account key file.
    # We'll assume the environment variable is set or we are in production.
    try:
        client = firestore.Client(project=project_id)
        logger.info(f"Firestore client initialized for project: {project_id}")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Firestore client: {e}")
        raise

class Brain:
    """The Brain class encapsulates all Firestore operations."""

    def __init__(self, firestore_client: firestore.Client):
        self.db = firestore_client
        self.client_configs_collection = "client_configs"
        self.oracle_insights_collection = "oracle_insights"
        self.system_health_collection = "system_health"

    def set_client_config(self, client_id: str, config: Dict[str, Any]) -> None:
        """Store or update a client's configuration."""
        try:
            doc_ref = self.db.collection(self.client_configs_collection).document(client_id)
            doc_ref.set(config, merge=True)
            logger.info(f"Client config set for client: {client_id}")
        except Exception as e:
            logger.error(f"Error setting client config for {client_id}: {e}")
            raise

    def get_client_config(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a client's configuration."""
        try:
            doc_ref = self.db.collection(self.client_configs_collection).document(client_id)
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
            else:
                return None
        except Exception as e:
            logger.error(f"Error getting client config for {client_id}: {e}")
            return None

    def store_insight(self, client_id: str, insight: Dict[str, Any]) -> str:
        """Store an insight in the Oracle Insights collection and return the document ID."""
        try:
            # Add timestamp if not present
            if "timestamp" not in insight:
                insight["timestamp"] = datetime.utcnow()
            # Add client_id
            insight["client_id"] = client_id
            doc_ref = self.db.collection(self.oracle_insights_collection).document()
            doc_ref.set(insight)
            logger.info(f"Insight stored for client: {client_id}")
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error storing insight for {client_id}: {e}")
            raise

    def get_latest_insight(self, client_id: str = "default") -> Optional[Dict[str, Any]]:
        """Retrieve the latest insight for a client."""
        try:
            insights_ref = self.db.collection(self.oracle_insights_collection)
            query = insights_ref.where("client_id", "==", client_id).order_by("timestamp", direction=firestore.Query.DESCENDING).limit(1)
            results = query.stream()
            for doc in results:
                return doc.to_dict()
            return None
        except Exception as e:
            logger.error(f"Error getting latest insight for {client_id}: {e}")
            return None

    def log_system_health(self, metric: Dict[str, Any]) -> None:
        """Log a system health metric."""
        try:
            metric["timestamp"] = datetime.utcnow()
            doc_ref = self.db.collection(self.system_health_collection).document()
            doc_ref.set(metric)
        except Exception as e:
            logger.error(f"Error logging system health: {e}")
            raise