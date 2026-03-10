"""
Main FastAPI application for the Magnetic Oracle.
This is the entry point for the service.
"""

import os
import logging
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings

from brain import get_firestore_client, Brain
from revelation_engine import RevelationEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    """Application settings."""
    project_id: str = os.getenv("PROJECT_ID", "curiosity-oracle-prod")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    stripe_api_key: str = os.getenv("STRIPE_API_KEY", "")
    stripe_webhook_secret: str = os.getenv("STRIPE_WEBHOOK_SECRET", "")

    class Config:
        env_file = ".env"

settings = Settings()

# Initialize Firebase and Firestore
firestore_client = get_firestore_client(settings.project_id)
brain = Brain(firestore_client)

# Initialize the Revelation Engine
revelation_engine = RevelationEngine(brain, settings.openai_api_key)

app = FastAPI(title="Magnetic Oracle", version="0.1.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency to get the brain instance
def get_brain():
    return brain

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, brain: Brain = Depends(get_brain)):
    """Main dashboard for the client."""
    # Fetch the latest insight from the brain
    latest_insight = brain.get_latest_insight()
    return templates.TemplateResponse("dashboard.html", {"request": request, "insight": latest_insight})

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Magnetic Oracle"}

@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks for payment events."""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')

    # Verify the webhook signature and process the event
    # This is a placeholder. In production, we would use the Stripe SDK to verify the webhook.
    # For now, we'll just log the event.
    logger.info(f"Stripe webhook received: {payload}")
    return {"status": "received"}

@app.post("/webhook/intercom")
async def intercom_webhook(request: Request):
    """Handle Intercom webhooks for new conversations."""
    # This is a placeholder for future integration.
    data = await request.json()
    logger.info(f"Intercom webhook received: {data}")
    return {"status": "received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)