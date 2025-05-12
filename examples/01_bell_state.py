import qsim.system
import qsim.gates

# Create a two-bit quantum system
system = qsim.system.System(2)

# Apply the Hadamard gate to the zeroth bit
hadamard_0 = qsim.gates.get_hadamard(0, 2)
system.apply_gate(hadamard_0)
print(system.state)

# Apply the CNOT gate
cnot = qsim.gates.get_cnot(1, 0, 2)
system.apply_gate(cnot)
print(system.state)

print(system._get_probabilities())