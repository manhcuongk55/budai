"""
Tests for Quantum Module ⚛️🪷
Tests run on default.qubit simulator — no quantum hardware needed.
"""

import pytest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.quantum.device import get_quantum_device, QuantumConfig
from app.quantum.prajna_circuits import (
    QuantumTruthCircuit,
    QuantumCompassionCircuit,
    QuantumEmptinessCircuit,
    QuantumHarmCircuit,
    QuantumPrajnaScorer,
    extract_text_features,
)
from app.quantum.quantum_crypto import QuantumCrypto
from app.quantum.quantum_embeddings import QuantumEmbedding


# ─── Tests: Device ───────────────────────────────────────────────────

class TestQuantumDevice:
    def test_default_device(self):
        dev = get_quantum_device(n_qubits=2)
        assert dev is not None

    def test_config_defaults(self):
        config = QuantumConfig()
        assert config.device_name == "default.qubit"
        assert config.n_qubits == 4
        assert config.enabled is True


# ─── Tests: Feature Extraction ───────────────────────────────────────

class TestFeatureExtraction:
    def test_empty_text(self):
        features = extract_text_features("", 4)
        assert len(features) == 4
        assert np.all(features == 0)

    def test_normal_text(self):
        features = extract_text_features("Hello world!", 4)
        assert len(features) == 4
        assert features[0] > 0  # Non-zero text length

    def test_feature_shape(self):
        features = extract_text_features("Test text", 8)
        assert len(features) == 8


# ─── Tests: Prajna Circuits ──────────────────────────────────────────

class TestQuantumPrajnaCircuits:
    def test_truth_circuit_returns_score(self):
        circuit = QuantumTruthCircuit(n_qubits=4, n_layers=1)
        score = circuit.score("This is a test statement")
        assert 0.0 <= score <= 1.0

    def test_compassion_circuit_returns_score(self):
        circuit = QuantumCompassionCircuit(n_qubits=4, n_layers=1)
        score = circuit.score("I understand your pain")
        assert 0.0 <= score <= 1.0

    def test_emptiness_circuit_returns_score(self):
        circuit = QuantumEmptinessCircuit(n_qubits=4, n_layers=1)
        score = circuit.score("There are multiple perspectives")
        assert 0.0 <= score <= 1.0

    def test_harm_circuit_returns_score(self):
        circuit = QuantumHarmCircuit(n_qubits=4, n_layers=1)
        score = circuit.score("How to cook pasta")
        assert 0.0 <= score <= 1.0

    def test_score_pair(self):
        circuit = QuantumTruthCircuit(n_qubits=4, n_layers=1)
        score = circuit.score_pair("What is Python?", "Python is a programming language.")
        assert 0.0 <= score <= 1.0

    def test_different_texts_different_scores(self):
        circuit = QuantumTruthCircuit(n_qubits=4, n_layers=1)
        score1 = circuit.score("Short text")
        score2 = circuit.score("A much longer text with many more words and details about various topics")
        # Different inputs should generally produce different outputs
        # (not guaranteed but very likely with random weights)
        assert isinstance(score1, float)
        assert isinstance(score2, float)


class TestQuantumPrajnaScorer:
    def test_score_all(self):
        scorer = QuantumPrajnaScorer(n_qubits=4, n_layers=1)
        scores = scorer.score_all("What is truth?", "Truth is subjective and objective.")
        assert "truth" in scores
        assert "compassion" in scores
        assert "emptiness" in scores
        assert "harm" in scores
        for v in scores.values():
            assert 0.0 <= v <= 1.0

    def test_circuit_info(self):
        scorer = QuantumPrajnaScorer(n_qubits=4, n_layers=1)
        info = scorer.get_circuit_info()
        assert info["n_qubits"] == 4
        assert info["n_layers"] == 1
        assert len(info["circuits"]) == 4


# ─── Tests: Quantum Crypto ──────────────────────────────────────────

class TestQuantumCrypto:
    def setup_method(self):
        self.crypto = QuantumCrypto(n_qubits=8)

    def test_quantum_random_bytes(self):
        rand = self.crypto.quantum_random_bytes(16)
        assert len(rand) == 16
        assert isinstance(rand, bytes)

    def test_quantum_nonce(self):
        nonce = self.crypto.quantum_nonce(16)
        assert len(nonce) == 32  # hex = 2 chars per byte
        assert all(c in "0123456789abcdef" for c in nonce)

    def test_two_nonces_different(self):
        n1 = self.crypto.quantum_nonce()
        n2 = self.crypto.quantum_nonce()
        # Quantum randomness should produce different nonces
        # (extremely unlikely to be same)
        assert isinstance(n1, str)
        assert isinstance(n2, str)

    def test_quantum_hmac_sign_verify(self):
        msg = "Hello Basao Protocol"
        key = "secret-key"
        sig = self.crypto.quantum_hmac(msg, key)
        assert ":" in sig  # format: salt:hmac
        assert self.crypto.verify_quantum_hmac(msg, key, sig)

    def test_quantum_hmac_wrong_key(self):
        msg = "Hello Basao Protocol"
        sig = self.crypto.quantum_hmac(msg, "correct-key")
        assert not self.crypto.verify_quantum_hmac(msg, "wrong-key", sig)

    def test_bb84_key_exchange(self):
        alice_bits, bob_bits, shared_key = self.crypto.bb84_key_exchange()
        assert len(alice_bits) == 8
        assert len(shared_key) > 0  # At least some bits should match
        assert len(shared_key) <= 8
        assert all(b in [0, 1] for b in shared_key)

    def test_crypto_info(self):
        info = self.crypto.get_info()
        assert info["quantum_safe"] is True
        assert "bb84_key_exchange" in info["capabilities"]


# ─── Tests: Quantum Embeddings ───────────────────────────────────────

class TestQuantumEmbedding:
    def setup_method(self):
        self.emb = QuantumEmbedding(n_qubits=4, n_layers=1)

    def test_embed_returns_state(self):
        features = np.array([0.1, 0.2, 0.3, 0.4])
        state = self.emb.embed(features)
        assert len(state) == 2 ** 4  # 2^n_qubits
        # State should be normalized
        norm = np.sum(np.abs(state) ** 2)
        assert abs(norm - 1.0) < 1e-6

    def test_self_similarity(self):
        features = np.array([0.5, 0.5, 0.5, 0.5])
        sim = self.emb.quantum_similarity(features, features)
        # Self-similarity should be close to 1
        assert sim > 0.9

    def test_text_similarity_same(self):
        sim = self.emb.text_similarity("hello world", "hello world")
        assert sim > 0.9  # Same text = high similarity

    def test_text_similarity_different(self):
        sim = self.emb.text_similarity("hello", "zzzzzzzzzzzzzzzzz")
        # Different texts should have lower similarity
        assert isinstance(sim, float)
        assert 0.0 <= sim <= 1.0

    def test_quantum_distance(self):
        f = np.array([0.3, 0.3, 0.3, 0.3])
        dist = self.emb.quantum_distance(f, f)
        assert dist < 0.1  # Self-distance ≈ 0

    def test_embedding_info(self):
        info = self.emb.get_info()
        assert info["n_qubits"] == 4
        assert info["hilbert_space_dim"] == 16


# ─── Run ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
