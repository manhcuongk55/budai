"""
Pydantic models for ZK Truth Proofs.
Structurally compatible with standard zk-SNARK outputs (Groth16/Plonk).
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ZKPublicSignals(BaseModel):
    """
    Public signals (inputs/outputs) for the ZK Circuit.
    This is what the verifier sees. It does NOT contain the private context.
    """
    # Hash of the user's question (to prove the proof is for THIS question)
    question_hash: str = Field(description="SHA-256 hash of the question")
    # Hash of the AI's answer
    answer_hash: str = Field(description="SHA-256 hash of the answer")
    
    # Public claims about the scores
    truth_score_min: float = Field(default=0.6, description="Claim: Truth score >= this")
    harm_score_max: float = Field(default=0.3, description="Claim: Harm score <= this")
    
    # Boolean claim
    is_prajna_compliant: int = Field(default=1, description="1 if compliant, 0 otherwise")
    
    # Timestamp to prevent replay of old proofs
    timestamp: str = Field(description="ISO format timestamp")


class ZKProof(BaseModel):
    """
    Simulated ZK-SNARK Proof.
    Matches the structure of SnarkJS / Circom outputs.
    """
    pi_a: List[str] = Field(description="Point A on elliptic curve (G1)")
    pi_b: List[List[str]] = Field(description="Point B on elliptic curve (G2)")
    pi_c: List[str] = Field(description="Point C on elliptic curve (G1)")
    protocol: str = Field(default="groth16", description="Proving system used")
    curve: str = Field(default="bn128", description="Elliptic curve used")
    
    public_signals: ZKPublicSignals = Field(description="The public inputs/outputs")
    
    def model_dump_json(self, *args, **kwargs):
        # Flatten signals for standard snarkjs compatibility when dumping
        data = super().model_dump(*args, **kwargs)
        signals = data.pop("public_signals")
        # In real snarkjs, publicSignals is an array of strings representing field elements
        data["publicSignals"] = [
            str(signals["question_hash"]),
            str(signals["answer_hash"]),
            str(int(signals["truth_score_min"] * 100)),
            str(int(signals["harm_score_max"] * 100)),
            str(signals["is_prajna_compliant"]),
            str(signals["timestamp"])
        ]
        # Store original struct in metadata for our app
        data["_meta_signals"] = signals
        import json
        return json.dumps(data)
