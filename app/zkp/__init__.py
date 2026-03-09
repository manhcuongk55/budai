"""
Zero-Knowledge Proof of Truth (ZK-PoT) 🪷🔐
Inspired by zk-credit-analysis, this module provides cryptographic proofs
that an AI response passed the Prajna Truth & Compassion filters,
without exposing the underlying proprietary source documents or model weights.
"""

from app.zkp.models import ZKProof, ZKPublicSignals
from app.zkp.prover import PrajnaZKProver
from app.zkp.verifier import verify_zk_proof

__all__ = ["ZKProof", "ZKPublicSignals", "PrajnaZKProver", "verify_zk_proof"]
