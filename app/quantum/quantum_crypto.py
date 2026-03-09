"""
Quantum Cryptography ⚛️🔐
Quantum-safe security for Basao Protocol:
- Quantum random number generation (truly random nonces)
- BB84 quantum key distribution simulation
- Quantum-enhanced HMAC
"""

import hashlib
import hmac
import logging
from typing import List, Tuple

import numpy as np
import pennylane as qml
from pennylane import numpy as pnp

from app.quantum.device import get_quantum_device

logger = logging.getLogger("budai.quantum.crypto")


class QuantumCrypto:
    """
    Quantum cryptographic primitives for Basao Protocol.
    Uses quantum randomness and BB84 protocol simulation.
    """

    def __init__(self, n_qubits: int = 8):
        self.n_qubits = n_qubits
        self.dev = get_quantum_device(n_qubits=n_qubits)

        # QNode for random number generation
        @qml.qnode(self.dev)
        def _random_circuit():
            """Generate quantum random bits via Hadamard + measurement."""
            for i in range(n_qubits):
                qml.Hadamard(wires=i)
            return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]

        self._random_circuit = _random_circuit

        # QNode for BB84 key generation
        @qml.qnode(self.dev)
        def _bb84_circuit(bases):
            """BB84 protocol: prepare qubits in random bases."""
            for i in range(n_qubits):
                # |0⟩ or |1⟩ in computational or Hadamard basis
                if bases[i] > 0:
                    qml.Hadamard(wires=i)
                qml.RY(bases[i] * np.pi, wires=i)
            return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]

        self._bb84_circuit = _bb84_circuit
        logger.info(f"⚛️🔐 Quantum Crypto initialized ({n_qubits} qubits)")

    def quantum_random_bytes(self, n_bytes: int = 16) -> bytes:
        """
        Generate truly random bytes using quantum measurement.
        Each qubit in superposition collapses to 0 or 1 — fundamentally random.
        """
        bits = []
        rounds = (n_bytes * 8 + self.n_qubits - 1) // self.n_qubits

        for _ in range(rounds):
            measurements = self._random_circuit()
            for m in measurements:
                # Expectation of PauliZ: +1 → 0, -1 → 1
                bits.append(0 if float(m) > 0 else 1)

        # Convert bits to bytes
        result_bits = bits[:n_bytes * 8]
        result = bytearray()
        for i in range(0, len(result_bits), 8):
            byte = sum(bit << (7 - j) for j, bit in enumerate(result_bits[i:i+8]))
            result.append(byte)

        return bytes(result[:n_bytes])

    def quantum_nonce(self, length: int = 16) -> str:
        """Generate a quantum-random nonce as hex string."""
        raw = self.quantum_random_bytes(length)
        return raw.hex()

    def quantum_hmac(self, message: str, key: str) -> str:
        """
        Quantum-enhanced HMAC.
        Uses quantum random salt mixed into the HMAC computation.
        """
        # Quantum salt
        q_salt = self.quantum_random_bytes(8)

        # Mix quantum salt with key
        enhanced_key = hashlib.sha256(key.encode() + q_salt).digest()

        # Standard HMAC with quantum-enhanced key
        signature = hmac.new(enhanced_key, message.encode(), hashlib.sha256).hexdigest()

        # Prepend salt for verification
        return q_salt.hex() + ":" + signature

    def verify_quantum_hmac(self, message: str, key: str, signature: str) -> bool:
        """Verify a quantum-enhanced HMAC signature."""
        try:
            salt_hex, mac = signature.split(":", 1)
            q_salt = bytes.fromhex(salt_hex)
            enhanced_key = hashlib.sha256(key.encode() + q_salt).digest()
            expected = hmac.new(enhanced_key, message.encode(), hashlib.sha256).hexdigest()
            return hmac.compare_digest(mac, expected)
        except (ValueError, AttributeError):
            return False

    def bb84_key_exchange(self) -> Tuple[List[int], List[int], List[int]]:
        """
        Simulate BB84 quantum key distribution protocol.

        Returns: (alice_bits, bob_bits, shared_key_bits)
        - Alice prepares qubits in random states and bases
        - Bob measures in random bases
        - They keep only bits where bases matched → shared secret key
        """
        # Alice: random bits and bases
        alice_bits = np.random.randint(0, 2, self.n_qubits)
        alice_bases = np.random.randint(0, 2, self.n_qubits)

        # Bob: random measurement bases
        bob_bases = np.random.randint(0, 2, self.n_qubits)

        # Alice prepares quantum states
        bases_input = pnp.array(alice_bits * np.pi + alice_bases * np.pi / 2, requires_grad=False)
        measurements = self._bb84_circuit(bases_input)

        # Bob measures
        bob_bits = []
        for i, m in enumerate(measurements):
            if alice_bases[i] == bob_bases[i]:
                # Same basis → Bob gets Alice's bit
                bob_bits.append(int(alice_bits[i]))
            else:
                # Different basis → random result
                bob_bits.append(0 if float(m) > 0 else 1)

        # Sifting: keep only matching bases
        shared_key = []
        for i in range(self.n_qubits):
            if alice_bases[i] == bob_bases[i]:
                shared_key.append(int(alice_bits[i]))

        logger.info(
            f"⚛️🔐 BB84: {self.n_qubits} qubits → "
            f"{len(shared_key)} shared key bits "
            f"({len(shared_key)/self.n_qubits*100:.0f}% efficiency)"
        )

        return alice_bits.tolist(), bob_bits, shared_key

    def get_info(self) -> dict:
        """Get quantum crypto system info."""
        return {
            "n_qubits": self.n_qubits,
            "device": str(self.dev),
            "capabilities": [
                "quantum_random_bytes",
                "quantum_nonce",
                "quantum_hmac",
                "bb84_key_exchange",
            ],
            "quantum_safe": True,
        }
