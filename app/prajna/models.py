"""Prajna Data Models — Pydantic schemas for the Bát Nhã filter system."""

from enum import Enum
from typing import List, Optional
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
    """Final result from the Prajna Network filter."""
    action: PrajnaAction = Field(description="Final decision: pass/rewrite/reject")
    original_answer: str = Field(description="The original AI response before filtering")
    final_answer: str = Field(description="The final response after Prajna filtering")
    total_attempts: int = Field(default=1, description="Number of attempts (1=no rewrite)")
    scores: List[PrajnaScore] = Field(description="Final scores from all classifiers")
    audit_log: List[PrajnaAudit] = Field(default_factory=list, description="Full audit trail")
    prajna_passed: bool = Field(description="Whether the final answer passed all checks")

    @property
    def summary(self) -> dict:
        """Quick summary of Prajna scores."""
        return {s.classifier: {"score": s.score, "passed": s.passed} for s in self.scores}
