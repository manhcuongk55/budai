"""
Data models for Berty P2P integration.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class BertyMessage(BaseModel):
    """Incoming encrypted message from Berty P2P network."""
    account_id: str = Field(description="Anonymous local account ID")
    conversation_pk: str = Field(description="Berty Conversation Public Key")
    message_type: str = Field(default="text", description="Type of message")
    payload: str = Field(description="The decrypted text content")
    timestamp: str = Field(description="ISO timestamp of receipt")


class BertyResponse(BaseModel):
    """Outgoing response back to Berty P2P network."""
    conversation_pk: str = Field(description="Target Conversation Public Key")
    payload: str = Field(description="budAI response text")
    action_taken: str = Field(description="Prajna Action (PASS/REWRITE/REJECT)")
    zk_proof: Optional[Dict[str, Any]] = Field(default=None, description="Optional ZK-PoT")
    
    # We DO NOT include the original prompt or user identifier in the response object
    # to prevent accidental logging upstream.
