"""
Quantum Prajna Circuits ⚛️🪷
Variational quantum circuits for scoring AI responses against 4 Bát Nhã principles.
Each circuit encodes text features → quantum rotations → entanglement → measurement → score.
"""

import logging
import numpy as np
from typing import List, Optional

import pennylane as qml
from pennylane import numpy as pnp

from app.quantum.device import get_quantum_device, quantum_config

logger = logging.getLogger("budai.quantum.prajna")


# ─── Feature Extraction (Classical → Quantum) ────────────────────────

def extract_text_features(text: str, n_features: int = 4) -> np.ndarray:
    """
    Extract simple numerical features from text for quantum encoding.
    Maps text properties to angles [0, 2π] for quantum rotations.

    Features:
    - f0: Text length (normalized)
    - f1: Question mark ratio (uncertainty indicator)
    - f2: Exclamation ratio (intensity indicator)
    - f3: Average word length (complexity indicator)
    """
    if not text:
        return np.zeros(n_features)

    text_len = min(len(text) / 1000.0, 1.0)  # Normalized to [0,1]

    chars = list(text)
    question_ratio = chars.count('?') / max(len(chars), 1)
    exclaim_ratio = chars.count('!') / max(len(chars), 1)

    words = text.split()
    avg_word_len = np.mean([len(w) for w in words]) / 15.0 if words else 0.0
    avg_word_len = min(avg_word_len, 1.0)

    features = np.array([text_len, question_ratio, exclaim_ratio, avg_word_len])

    # Scale to [0, 2π] for quantum rotations
    features = features * 2 * np.pi

    # Pad or truncate to n_features
    if len(features) < n_features:
        features = np.pad(features, (0, n_features - len(features)))
    return features[:n_features]


# ─── Base Quantum Circuit ────────────────────────────────────────────

class QuantumPrajnaCircuit:
    """Base class for Prajna quantum scoring circuits."""

    name: str = "base"
    n_qubits: int = 4

    def __init__(self, n_qubits: int = 4, n_layers: int = 2):
        self.n_qubits = n_qubits
        self.n_layers = n_layers
        self.dev = get_quantum_device(n_qubits=n_qubits)

        # Trainable parameters (randomly initialized)
        n_params = n_layers * n_qubits * 3  # 3 rotations per qubit per layer
        self.weights = pnp.array(
            np.random.uniform(0, 2 * np.pi, size=n_params),
            requires_grad=True
        )

        # Build the quantum circuit
        self._circuit = qml.QNode(self._circuit_fn, self.dev)

    def _circuit_fn(self, features, weights):
        """
        Variational quantum circuit:
        1. Encode features into quantum state (amplitude encoding)
        2. Apply variational layers (trainable rotations + entanglement)
        3. Measure expectation value
        """
        n_params_per_layer = self.n_qubits * 3
        weights_reshaped = weights.reshape(self.n_layers, self.n_qubits, 3)

        # Step 1: Feature encoding — embed classical data into quantum state
        for i in range(self.n_qubits):
            qml.RX(features[i], wires=i)
            qml.RY(features[i] * 0.5, wires=i)

        # Step 2: Variational layers — trainable quantum neural network
        for layer in range(self.n_layers):
            # Rotations (trainable)
            for qubit in range(self.n_qubits):
                qml.RX(weights_reshaped[layer, qubit, 0], wires=qubit)
                qml.RY(weights_reshaped[layer, qubit, 1], wires=qubit)
                qml.RZ(weights_reshaped[layer, qubit, 2], wires=qubit)

            # Entanglement — creates quantum correlations between qubits
            for qubit in range(self.n_qubits - 1):
                qml.CNOT(wires=[qubit, qubit + 1])
            # Ring entanglement
            if self.n_qubits > 2:
                qml.CNOT(wires=[self.n_qubits - 1, 0])

        # Step 3: Measurement — expectation value of PauliZ on first qubit
        return qml.expval(qml.PauliZ(0))

    def score(self, text: str) -> float:
        """
        Score a text through the quantum circuit.
        Returns float in [0, 1].
        """
        features = extract_text_features(text, self.n_qubits)
        raw = float(self._circuit(features, self.weights))
        # Map from [-1, 1] (PauliZ expectation) to [0, 1]
        return (raw + 1.0) / 2.0

    def score_pair(self, question: str, answer: str) -> float:
        """Score a question-answer pair by combining their features."""
        q_features = extract_text_features(question, self.n_qubits // 2)
        a_features = extract_text_features(answer, self.n_qubits - self.n_qubits // 2)
        features = np.concatenate([q_features, a_features])[:self.n_qubits]
        raw = float(self._circuit(features, self.weights))
        return (raw + 1.0) / 2.0


# ─── 4 Prajna Quantum Circuits ───────────────────────────────────────

class QuantumTruthCircuit(QuantumPrajnaCircuit):
    """
    Truth Circuit ⚛️🔍
    Quantum scoring for truthfulness.
    Uses Hadamard gates for superposition (representing uncertainty awareness).
    """
    name = "quantum_truth"

    def _circuit_fn(self, features, weights):
        weights_reshaped = weights.reshape(self.n_layers, self.n_qubits, 3)

        # Hadamard — put qubits in superposition (representing all possibilities)
        for i in range(self.n_qubits):
            qml.Hadamard(wires=i)

        # Feature encoding
        for i in range(self.n_qubits):
            qml.RY(features[i], wires=i)

        # Variational layers
        for layer in range(self.n_layers):
            for qubit in range(self.n_qubits):
                qml.RX(weights_reshaped[layer, qubit, 0], wires=qubit)
                qml.RY(weights_reshaped[layer, qubit, 1], wires=qubit)
                qml.RZ(weights_reshaped[layer, qubit, 2], wires=qubit)
            for qubit in range(self.n_qubits - 1):
                qml.CNOT(wires=[qubit, qubit + 1])
            if self.n_qubits > 2:
                qml.CNOT(wires=[self.n_qubits - 1, 0])

        return qml.expval(qml.PauliZ(0))


class QuantumCompassionCircuit(QuantumPrajnaCircuit):
    """
    Compassion Circuit ⚛️💛
    Uses SWAP gates for qubit interaction (representing empathy/connection).
    """
    name = "quantum_compassion"

    def _circuit_fn(self, features, weights):
        weights_reshaped = weights.reshape(self.n_layers, self.n_qubits, 3)

        # Feature encoding
        for i in range(self.n_qubits):
            qml.RX(features[i], wires=i)

        # Variational layers with SWAP (empathy = exchanging states)
        for layer in range(self.n_layers):
            for qubit in range(self.n_qubits):
                qml.RX(weights_reshaped[layer, qubit, 0], wires=qubit)
                qml.RY(weights_reshaped[layer, qubit, 1], wires=qubit)
                qml.RZ(weights_reshaped[layer, qubit, 2], wires=qubit)

            # SWAP pairs — empathic entanglement
            for qubit in range(0, self.n_qubits - 1, 2):
                qml.SWAP(wires=[qubit, qubit + 1])

            # CNOT chain
            for qubit in range(self.n_qubits - 1):
                qml.CNOT(wires=[qubit, qubit + 1])

        return qml.expval(qml.PauliZ(0))


class QuantumEmptinessCircuit(QuantumPrajnaCircuit):
    """
    Emptiness Circuit ⚛️🌀
    Uses maximum superposition (GHZ state) representing non-attachment to any single view.
    The GHZ state is equally distributed — no single outcome is privileged.
    """
    name = "quantum_emptiness"

    def _circuit_fn(self, features, weights):
        weights_reshaped = weights.reshape(self.n_layers, self.n_qubits, 3)

        # GHZ state preparation — maximum entanglement (Tính Không = all interconnected)
        qml.Hadamard(wires=0)
        for i in range(1, self.n_qubits):
            qml.CNOT(wires=[0, i])

        # Feature encoding on top of GHZ state
        for i in range(self.n_qubits):
            qml.RY(features[i], wires=i)

        # Variational layers
        for layer in range(self.n_layers):
            for qubit in range(self.n_qubits):
                qml.RX(weights_reshaped[layer, qubit, 0], wires=qubit)
                qml.RY(weights_reshaped[layer, qubit, 1], wires=qubit)
                qml.RZ(weights_reshaped[layer, qubit, 2], wires=qubit)
            for qubit in range(self.n_qubits - 1):
                qml.CNOT(wires=[qubit, qubit + 1])

        return qml.expval(qml.PauliZ(0))


class QuantumHarmCircuit(QuantumPrajnaCircuit):
    """
    Harm Detection Circuit ⚛️🛡️
    Uses quantum interference to amplify harmful patterns (Grover-inspired).
    """
    name = "quantum_harm"

    def _circuit_fn(self, features, weights):
        weights_reshaped = weights.reshape(self.n_layers, self.n_qubits, 3)

        # Feature encoding
        for i in range(self.n_qubits):
            qml.RX(features[i], wires=i)

        # Variational layers with phase kickback (amplifies harm signals)
        for layer in range(self.n_layers):
            for qubit in range(self.n_qubits):
                qml.RX(weights_reshaped[layer, qubit, 0], wires=qubit)
                qml.RY(weights_reshaped[layer, qubit, 1], wires=qubit)
                qml.RZ(weights_reshaped[layer, qubit, 2], wires=qubit)

            # CZ gates — phase interference (detects harmful correlations)
            for qubit in range(self.n_qubits - 1):
                qml.CZ(wires=[qubit, qubit + 1])

            # Grover-like diffusion
            for qubit in range(self.n_qubits):
                qml.Hadamard(wires=qubit)
                qml.PauliZ(wires=qubit)
                qml.Hadamard(wires=qubit)

        return qml.expval(qml.PauliZ(0))


# ─── Unified Quantum Prajna Scorer ───────────────────────────────────

class QuantumPrajnaScorer:
    """
    Unified quantum scorer — runs all 4 Prajna circuits.
    Can be used alongside or instead of the classical AI-as-Judge classifiers.
    """

    def __init__(self, n_qubits: int = 4, n_layers: int = 2):
        self.truth = QuantumTruthCircuit(n_qubits, n_layers)
        self.compassion = QuantumCompassionCircuit(n_qubits, n_layers)
        self.emptiness = QuantumEmptinessCircuit(n_qubits, n_layers)
        self.harm = QuantumHarmCircuit(n_qubits, n_layers)
        logger.info("⚛️🪷 Quantum Prajna Scorer initialized (4 circuits)")

    def score_all(self, question: str, answer: str) -> dict:
        """
        Score a Q&A pair through all 4 quantum circuits.
        Returns dict of scores [0, 1].
        """
        scores = {
            "truth": self.truth.score_pair(question, answer),
            "compassion": self.compassion.score_pair(question, answer),
            "emptiness": self.emptiness.score_pair(question, answer),
            "harm": self.harm.score_pair(question, answer),
        }

        logger.info(
            f"⚛️ Quantum scores: "
            f"T={scores['truth']:.3f} "
            f"C={scores['compassion']:.3f} "
            f"E={scores['emptiness']:.3f} "
            f"H={scores['harm']:.3f}"
        )
        return scores

    def get_circuit_info(self) -> dict:
        """Get info about quantum circuits."""
        return {
            "n_qubits": self.truth.n_qubits,
            "n_layers": self.truth.n_layers,
            "device": str(self.truth.dev),
            "circuits": ["truth", "compassion", "emptiness", "harm"],
            "trainable_params": len(self.truth.weights) * 4,
        }
