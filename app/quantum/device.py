"""
Quantum Device Manager — PennyLane device abstraction.
Default: simulator (default.qubit). Switchable to real quantum hardware.
"""

import logging
from typing import Optional
from pydantic import BaseModel, Field

import pennylane as qml

logger = logging.getLogger("budai.quantum")


class QuantumConfig(BaseModel):
    """Configuration for quantum computing backend."""
    # Device settings
    device_name: str = Field(default="default.qubit",
        description="PennyLane device: default.qubit, qiskit.ibmq, braket.aws.qubit, etc.")
    n_qubits: int = Field(default=4, ge=1, le=32,
        description="Number of qubits per circuit")
    shots: Optional[int] = Field(default=None,
        description="Number of measurement shots. None = analytic (simulator only)")

    # Hardware settings (for real quantum devices)
    ibm_token: Optional[str] = Field(default=None, description="IBM Quantum API token")
    aws_device_arn: Optional[str] = Field(default=None, description="AWS Braket device ARN")

    # Training settings
    learning_rate: float = Field(default=0.01, description="Optimizer learning rate")
    n_layers: int = Field(default=2, ge=1, le=10, description="Variational circuit depth")

    # Feature
    enabled: bool = Field(default=True, description="Enable quantum processing")


# Global config
quantum_config = QuantumConfig()


def get_quantum_device(
    n_qubits: Optional[int] = None,
    device_name: Optional[str] = None,
    shots: Optional[int] = None,
):
    """
    Get a PennyLane quantum device.

    Default: default.qubit simulator (runs anywhere, no hardware needed).
    For real quantum hardware, configure device_name:
      - "qiskit.ibmq" → IBM Quantum
      - "braket.aws.qubit" → Amazon Braket
      - "cirq.simulator" → Google Cirq
    """
    config = quantum_config
    name = device_name or config.device_name
    qubits = n_qubits or config.n_qubits
    s = shots or config.shots

    kwargs = {"wires": qubits}
    if s is not None:
        kwargs["shots"] = s

    try:
        dev = qml.device(name, **kwargs)
        logger.info(f"⚛️ Quantum device: {name} ({qubits} qubits)")
        return dev
    except Exception as e:
        logger.warning(f"⚛️ Failed to init {name}: {e}. Falling back to default.qubit")
        return qml.device("default.qubit", wires=qubits)
