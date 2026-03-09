"""
ZK Circuit Simulator.
Simulates a Circom circuit that verifies a set of scores against thresholds.
In production, this would be a compiled WASM/ZK-SNARK circuit.
"""

from typing import Dict

def simulate_prajna_circuit_witness(
    truth_score: float, 
    harm_score: float, 
    truth_min: float = 0.6, 
    harm_max: float = 0.3
) -> Dict[str, int]:
    """
    Simulate generating a ZK witness.
    A circuit in Circom asserts:
        assert(truth_score >= truth_min);
        assert(harm_score <= harm_max);
    
    If the assertions hold, it outputs { "is_valid": 1 }. 
    Otherwise, the proof generation fails.
    """
    
    # In a real ZK circuit, these would be field numbers (e.g. multiplied by 1000)
    t_score_int = int(truth_score * 1000)
    h_score_int = int(harm_score * 1000)
    t_min_int = int(truth_min * 1000)
    h_max_int = int(harm_max * 1000)
    
    # The circuit constraint logic
    is_valid = 1 if (t_score_int >= t_min_int and h_score_int <= h_max_int) else 0
    
    if not is_valid:
        raise ValueError("Circuit constraints not satisfied. Cannot generate proof.")
        
    return {
        "is_valid": is_valid,
        "t_score": t_score_int,
        "h_score": h_score_int
    }
