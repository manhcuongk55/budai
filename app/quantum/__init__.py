"""
Quantum Module 🪷⚛️ — PennyLane quantum computing integration for budAI.
Quantum-enhanced Prajna classifiers, crypto, and embeddings.
"""

from app.quantum.device import get_quantum_device, QuantumConfig
from app.quantum.prajna_circuits import (
    QuantumTruthCircuit,
    QuantumCompassionCircuit,
    QuantumEmptinessCircuit,
    QuantumHarmCircuit,
    QuantumPrajnaScorer,
)
from app.quantum.quantum_crypto import QuantumCrypto
from app.quantum.quantum_embeddings import QuantumEmbedding

__all__ = [
    "get_quantum_device", "QuantumConfig",
    "QuantumTruthCircuit", "QuantumCompassionCircuit",
    "QuantumEmptinessCircuit", "QuantumHarmCircuit",
    "QuantumPrajnaScorer",
    "QuantumCrypto", "QuantumEmbedding",
]
