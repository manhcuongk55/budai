"""Prajna Data Models — Pydantic schemas for the Bát Nhã filter system."""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class PrajnaAction(str, Enum):
    """Decision outcome from the Prajna Network."""
    PASS = "pass"           # All checks passed — send as-is
    REWRITE = "rewrite"     # Failed soft checks — rewrite with feedback
    REJECT = "reject"       # Failed harm check — refuse to answer


class PrajnaScore(BaseModel):
    """Score from a single Prajna classifier."""
    classifier: str = Field(description="Name of the classifier (truth/compassion/emptiness/harm)")
    score: float = Field(ge=0.0, le=1.0, description="Compliance score (0=fail, 1=perfect)")
    passed: bool = Field(description="Whether the score meets the threshold")
    feedback: str = Field(default="", description="Explanation and improvement suggestions")
    threshold: float = Field(description="The threshold used for this evaluation")


class PrajnaAudit(BaseModel):
    """Audit log entry for a single filter pass."""
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    attempt: int = Field(description="Attempt number (1=original, 2+=rewrite)")
    scores: List[PrajnaScore] = Field(description="Scores from all 4 classifiers")
    action: PrajnaAction = Field(description="Decision taken")
    rewrite_prompt: Optional[str] = Field(default=None, description="Prompt used for rewriting")


class PrajnaResult(BaseModel):
    """The final result of filtering an AI response through the Prajna network."""
    action: PrajnaAction = Field(description="The action taken (PASS, REWRITE, REJECT)")
    final_answer: str = Field(description="The final AI response (may be rewritten)")
    scores: List[PrajnaScore] = Field(description="Individual scores from all classifiers")
    prajna_passed: bool = Field(description="True if all classifiers passed")
    rewrite_attempts: int = Field(default=0, description="Number of rewrites performed")
    zk_proof: Optional[Dict[str, Any]] = Field(default=None, description="Zero-Knowledge Proof of Truth")
    audit_log: List[PrajnaAudit] = Field(default_factory=list, description="Full audit trail")

    @property
    def summary(self) -> dict:
        """Quick summary of Prajna scores."""
        return {s.classifier: {"score": s.score, "passed": s.passed} for s in self.scores}
