import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Configuration
    COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
    
    # Model Selection
    USE_COHERE = os.getenv("USE_COHERE", "true").lower() == "true"
    
    # RAG Configuration
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    MAX_RETRIEVAL_DOCS = int(os.getenv("MAX_RETRIEVAL_DOCS", "5"))
    
    # Classification Labels
    TOPIC_TAGS = [
        "How-to", "Product", "Connector", "Lineage", "API/SDK", 
        "SSO", "Glossary", "Best practices", "Sensitive data"
    ]
    
    SENTIMENT_LABELS = ["Frustrated", "Curious", "Angry", "Neutral"]
    PRIORITY_LABELS = ["P0 (High)", "P1 (Medium)", "P2 (Low)"]
    
    # Knowledge Base URLs
    ATLAN_DOCS_URL = "https://docs.atlan.com/"
    ATLAN_DEVELOPER_URL = "https://developer.atlan.com/"
