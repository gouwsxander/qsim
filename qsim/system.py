import numpy as np
from functools import reduce


class System:
    def __init__(self, n_bits: int | None = None, classical_state: np.ndarray | None = None):     
        """Initialize a quantum system with n qubits or starting in a specified classical state."""   
        if classical_state is None and n_bits is not None:
            classical_state = np.zeros(n_bits)
        elif n_bits is None and classical_state is not None:
            n_bits = len(classical_state)
        else:
            raise ValueError('Please assign either n_bits or initial_state.')

        x = np.zeros((n_bits, 2), dtype=complex)
        x[classical_state == 0, 0] = 1.0
        x[classical_state == 1, 1] = 1.0
        
        self.n_bits = n_bits
        self.state = reduce(np.kron, x)

    def _get_probabilities(self) -> np.ndarray:
        """Get the probability of collapsing into each possible classical state."""
        probabilities = (self.state.conj() * self.state).real
        return probabilities

    def measure(self):
        """Measure the state of the system."""
        probabilities = self._get_probabilities()

        next_state_idx = np.random.choice(np.arange(2**self.n_bits), p=probabilities)
        self.state = np.zeros(2**self.n_bits, dtype=complex)
        self.state[next_state_idx] = 1.0

    def apply_gate(self, gate: np.ndarray):
        """Apply a gate to your system."""
        self.state = gate @ self.state