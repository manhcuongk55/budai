"""Prajna Configuration — thresholds and settings for the Bát Nhã filter."""

from pydantic import BaseModel, Field


class PrajnaConfig(BaseModel):
    """Configuration for the Prajna Deep Learning Network."""

    # Enable/disable the entire Prajna filter
    enabled: bool = Field(default=True, description="Master switch for Prajna filtering")

    # Score thresholds (score must be >= threshold to pass)
    truth_threshold: float = Field(default=0.6, ge=0.0, le=1.0,
        description="Minimum truth score to pass")
    compassion_threshold: float = Field(default=0.5, ge=0.0, le=1.0,
        description="Minimum compassion score to pass")
    emptiness_threshold: float = Field(default=0.4, ge=0.0, le=1.0,
        description="Minimum emptiness/multi-perspective score to pass")
    harm_threshold: float = Field(default=0.3, ge=0.0, le=1.0,
        description="Maximum harm score allowed (INVERSE: lower = safer)")

    # Rewrite settings
    max_rewrite_attempts: int = Field(default=2, ge=0, le=5,
        description="Max times to rewrite before accepting or rejecting")

    # Judge model settings
    judge_temperature: float = Field(default=0.1,
        description="Temperature for judge LLM calls (low = deterministic)")
    judge_max_tokens: int = Field(default=512,
        description="Max tokens for judge responses")

    # Logging
    log_audit: bool = Field(default=True,
        description="Whether to log full audit trail")


# Global default config
prajna_config = PrajnaConfig()
