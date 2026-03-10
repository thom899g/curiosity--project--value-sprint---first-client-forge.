"""
Data Simulator: generates mock data for testing the Revelation Engine.
"""

import json
import csv
import random
from datetime import datetime, timedelta
from typing import Dict, Any

def generate_sample_intercom_conversations(file_path: str, num_conversations: int = 50) -> None:
    """Generate a sample Intercom conversations JSON file."""
    conversations = []
    for i in range(num_conversations):
        conversation = {
            "id": i,
            "user_id": random.randint(1000, 2000),
            "body": random.choice([
                "How do I integrate the API?",
                "Is there a discount for annual billing?",
                "I'm having trouble with the dashboard.",
                "When will feature X be available?",
                "I love your product!",
                "I'm considering canceling my subscription."
            ]),
            "created_at": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
            "tags": random.sample(["support", "billing", "feedback", "churn"], random.randint(1, 2))
        }
        conversations.append(conversation)

    with open(file_path, 'w') as f:
        json.dump(conversations, f, indent=2)

def generate_sample_stripe_customers(file_path: str, num_customers: int = 100) -> None:
    """Generate a sample Stripe customers CSV file."""
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['customer_id', 'email', 'subscription_status', 'created', 'total_revenue']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(num_customers):
            writer.writerow({
                'customer_id': f'cus_{i:03d}',
                'email': f'user{i}@example.com',
                'subscription_status': random.choice(['active', 'canceled', 'past_due']),
                'created': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
                'total_revenue': random.randint(1000, 10000)
            })

if __name__ == "__main__":
    generate_sample_intercom_conversations("sample_intercom_conversations.json")
    generate_sample_stripe_customers("sample_stripe_customers.csv")
    print("Sample data generated.")