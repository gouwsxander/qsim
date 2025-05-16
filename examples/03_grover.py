import numpy as np

import qsim.system
import qsim.gates

N_BITS = 4

# Create an oracle with a random key which we want to find
oracle = qsim.gates.get_oracle_gate(N_BITS, key=3)

# Create a n-bit quantum system
system = qsim.system.System(N_BITS)

# Apply the Hadamard gate to all gates
hadamard_all = qsim.gates.make_gate(
    {i: qsim.gates.H_1 for i in range(N_BITS)},
    N_BITS
)
system.apply_gate(hadamard_all)

diffusion = -qsim.gates.get_oracle_gate(N_BITS, state=system.state)

# Apply the oracle and diffusion operations
for i in range(int(np.pi / 4 * np.sqrt(2**N_BITS))):
    system.apply_gate(oracle)
    system.apply_gate(diffusion)

    # Investigate how system state changes with each step.
    print(system._get_probabilities())

