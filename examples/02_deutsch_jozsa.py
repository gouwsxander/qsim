from typing import Iterable

import numpy as np

import qsim.system
import qsim.gates

# One bit is reserved for the output
N_BITS = 3 + 1


def create_oracle(balanced: bool):
    """Deutsch--Jozsa oracle is either balanced or constant."""
    gate = np.eye(2**N_BITS, dtype=complex)

    swap_values = range(2**(N_BITS - 2)) if balanced else []
    for i in swap_values:
        j = i + 2**(N_BITS - 1)
        gate[i, i] = 0.
        gate[i, j] = 1.
        gate[j, i] = 1.
        gate[j, j] = 0.
    
    return gate


# Create system
system = qsim.system.System(N_BITS)

# Create useful gates
oracle = create_oracle(balanced=False)

flip_output = qsim.gates.get_x(0, N_BITS)

hadamard_all = qsim.gates.make_gate(
    {i: qsim.gates.H_1 for i in range(N_BITS)},
    N_BITS
)

hadamard_compute = qsim.gates.make_gate(
    {i: qsim.gates.H_1 for i in range(1, N_BITS)},
    N_BITS
)

# Perform Deutsch--Jozsa algorithm
system.apply_gate(flip_output)
system.apply_gate(hadamard_all)
system.apply_gate(oracle)
system.apply_gate(hadamard_compute)

# Measure
print(system._get_probabilities())

# If the oracle is constant, the compute bits will always be |0>
# Otherwise, they will never be |0>.