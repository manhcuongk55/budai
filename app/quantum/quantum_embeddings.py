"""
Quantum Embeddings ⚛️📐
Quantum feature maps for text similarity — potential exponential speedup
over classical methods for high-dimensional semantic comparison.
"""

import logging
from typing import List

import numpy as np
import pennylane as qml
from pennylane import numpy as pnp

from app.quantum.device import get_quantum_device

logger = logging.getLogger("budai.quantum.embeddings")


class QuantumEmbedding:
    """
    Quantum text embedding — maps classical embeddings into quantum Hilbert space.

    The quantum kernel trick: two vectors that are similar in classical space
    will have high overlap (fidelity) in quantum space. This can provide
    exponential advantage for certain similarity computations.
    """

    def __init__(self, n_qubits: int = 4, n_layers: int = 2):
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.dev = get_quantum_device(n_qubits=n_qubits)

        @qml.qnode(self.dev)
        def _embedding_circuit(features):
            """Angle embedding + entangling layers → quantum state."""
            # Angle embedding: encode features as rotation angles
            for i in range(n_qubits):
                qml.RY(features[i], wires=i)

            # Entangling layers for feature interaction
            for _ in range(n_layers):
                for i in range(n_qubits - 1):
                    qml.CNOT(wires=[i, i + 1])
                if n_qubits > 2:
                    qml.CNOT(wires=[n_qubits - 1, 0])

                for i in range(n_qubits):
                    qml.RY(features[i] * 0.5, wires=i)
                    qml.RZ(features[i] * 0.3, wires=i)

            return qml.state()

        self._embedding_circuit = _embedding_circuit

        @qml.qnode(self.dev)
        def _kernel_circuit(features1, features2):
            """
            Quantum kernel: measure overlap between two quantum embeddings.
            High overlap = high similarity.
            """
            # Embed first vector
            for i in range(n_qubits):
                qml.RY(features1[i], wires=i)
            for i in range(n_qubits - 1):
                qml.CNOT(wires=[i, i + 1])

            # Adjoint of second embedding (inverse)
            for i in reversed(range(n_qubits - 1)):
                qml.CNOT(wires=[i, i + 1])
            for i in range(n_qubits):
                qml.RY(-features2[i], wires=i)

            # Measure probability of all-zero state (= overlap)
            return qml.probs(wires=range(n_qubits))

        self._kernel_circuit = _kernel_circuit

        logger.info(f"⚛️📐 Quantum Embedding initialized ({n_qubits} qubits, {n_layers} layers)")

    def embed(self, features: np.ndarray) -> np.ndarray:
        """
        Embed a classical feature vector into quantum Hilbert space.
        Returns the full quantum state vector (2^n_qubits dimensional).
        """
        # Normalize to [0, π]
        features = self._normalize_features(features)
        state = self._embedding_circuit(features)
        return np.array(state)

    def quantum_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Compute quantum kernel similarity between two feature vectors.
        Uses the swap test / overlap method.
        Returns float in [0, 1] where 1 = identical.
        """
        f1 = self._normalize_features(vec1)
        f2 = self._normalize_features(vec2)
        probs = self._kernel_circuit(f1, f2)
        # Probability of all-zero state = |⟨ψ1|ψ2⟩|²
        similarity = float(probs[0])
        return similarity

    def batch_similarity(self, query: np.ndarray, candidates: List[np.ndarray]) -> List[float]:
        """Compute similarity of query against multiple candidates."""
        return [self.quantum_similarity(query, c) for c in candidates]

    def quantum_distance(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Quantum distance = 1 - quantum similarity."""
        return 1.0 - self.quantum_similarity(vec1, vec2)

    def text_to_quantum_features(self, text: str) -> np.ndarray:
        """
        Simple text → quantum features mapping.
        For production, use classical embedding (OpenAI, HuggingFace)
        then project into quantum space.
        """
        if not text:
            return np.zeros(self.n_qubits)

        # Simple character-level features
        chars = [ord(c) for c in text[:100]]
        n = self.n_qubits

        features = np.zeros(n)
        chunk_size = max(len(chars) // n, 1)
        for i in range(n):
            start = i * chunk_size
            end = min(start + chunk_size, len(chars))
            if start < len(chars):
                features[i] = np.mean(chars[start:end]) / 128.0 * np.pi

        return features

    def text_similarity(self, text1: str, text2: str) -> float:
        """Compute quantum similarity between two texts."""
        f1 = self.text_to_quantum_features(text1)
        f2 = self.text_to_quantum_features(text2)
        return self.quantum_similarity(f1, f2)

    def _normalize_features(self, features: np.ndarray) -> pnp.ndarray:
        """Normalize feature vector to [0, π] range for quantum encoding."""
        f = np.array(features, dtype=float)
        # Pad or truncate
        if len(f) < self.n_qubits:
            f = np.pad(f, (0, self.n_qubits - len(f)))
        f = f[:self.n_qubits]
        # Normalize to [0, π]
        if np.max(np.abs(f)) > 0:
            f = f / np.max(np.abs(f)) * np.pi
        return pnp.array(f, requires_grad=False)

    def get_info(self) -> dict:
        """Get quantum embedding info."""
        return {
            "n_qubits": self.n_qubits,
            "hilbert_space_dim": 2 ** self.n_qubits,
            "n_layers": self.n_layers,
            "device": str(self.dev),
        }
