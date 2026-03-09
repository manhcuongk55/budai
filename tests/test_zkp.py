"""
Tests for Zero-Knowledge Proofs of Truth 🪷🔐
Simulated cryptography verifying AI answers without exposing context.
"""

import pytest
import datetime
import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.zkp.models import ZKProof, ZKPublicSignals
from app.zkp.circuit_simulator import simulate_prajna_circuit_witness
from app.zkp.prover import PrajnaZKProver
from app.zkp.verifier import verify_zk_proof


class TestZkCircuitSimulator:
    def test_valid_scores_pass(self):
        witness = simulate_prajna_circuit_witness(truth_score=0.8, harm_score=0.1)
        assert witness["is_valid"] == 1
        assert witness["t_score"] == 800
        
    def test_low_truth_fails(self):
        with pytest.raises(ValueError, match="constraints not satisfied"):
            simulate_prajna_circuit_witness(truth_score=0.5, harm_score=0.1, truth_min=0.6)
            
    def test_high_harm_fails(self):
        with pytest.raises(ValueError, match="constraints not satisfied"):
            simulate_prajna_circuit_witness(truth_score=0.9, harm_score=0.5, harm_max=0.3)


class TestZkProver:
    def setup_method(self):
        self.prover = PrajnaZKProver(private_zkey="test_key_1")
        self.question = "What is gravity?"
        self.answer = "It is a fundamental interaction."
        
    def test_generate_valid_proof(self):
        proof = self.prover.generate_proof(self.question, self.answer, 0.9, 0.1)
        
        assert proof is not None
        assert isinstance(proof, ZKProof)
        assert len(proof.pi_a) == 3
        assert len(proof.pi_b) == 3
        assert len(proof.pi_b[0]) == 2
        
        # Verify public signals
        sig = proof.public_signals
        assert sig.truth_score_min == 0.6
        assert sig.is_prajna_compliant == 1
        
    def test_generate_proof_fails_on_bad_scores(self):
        proof = self.prover.generate_proof(self.question, self.answer, 0.2, 0.9)
        assert proof is None
        
    def test_dump_json_snarkjs_format(self):
        proof = self.prover.generate_proof(self.question, self.answer, 0.9, 0.1)
        dumped = json.loads(proof.model_dump_json())
        
        assert "pi_a" in dumped
        assert "publicSignals" in dumped
        assert len(dumped["publicSignals"]) == 6  # Flattened string array


class TestZkVerifier:
    def setup_method(self):
        self.prover = PrajnaZKProver(private_zkey="test_key_1")
        self.question = "Why is the sky blue?"
        self.answer = "Rayleigh scattering."
        self.proof = self.prover.generate_proof(self.question, self.answer, 0.8, 0.1)

    def test_valid_proof_verifies(self):
        assert verify_zk_proof(self.proof, self.question, self.answer) is True
        
    def test_wrong_question_fails(self):
        assert verify_zk_proof(self.proof, "Different question?", self.answer) is False
        
    def test_wrong_answer_fails(self):
        assert verify_zk_proof(self.proof, self.question, "Different answer") is False
        
    def test_expired_proof_fails(self):
        # Manually alter the timestamp to be 2 days old
        old_time = (datetime.datetime.utcnow() - datetime.timedelta(days=2)).isoformat()
        self.proof.public_signals.timestamp = old_time
        
        assert verify_zk_proof(self.proof, self.question, self.answer) is False
        
    def test_tampered_compliance_fails(self):
        self.proof.public_signals.is_prajna_compliant = 0
        assert verify_zk_proof(self.proof, self.question, self.answer) is False
        
    def test_tampered_proof_math_fails(self):
        # Tamper with the proof points
        self.proof.pi_a = ["1", "2"] # Missing 3rd element
        assert verify_zk_proof(self.proof, self.question, self.answer) is False

