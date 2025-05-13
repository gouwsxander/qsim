from functools import reduce
from typing import Iterable

import numpy as np

# One-qubit gates
I_1 = np.eye(2)
X_1 = np.array([[0., 1.], [1., 0.]])
Y_1 = np.array([[0., -1.j], [1.j, 0.]])
Z_1 = np.array([[1., 0.], [0., -1.]])
H_1 = np.array([[1., 1.], [1., -1.]]) / np.sqrt(2)
S_1 = np.array([[1., 0.], [0., 1.j]])
T_1 = np.array([[1., 0.], [0., np.exp(1.j * np.pi / 4)]])
OUTER_0_0 = np.array([[1., 0.], [0., 0.]])
OUTER_1_1 = np.array([[0., 0.], [0., 1.]])


def tensor_product(operators: Iterable[np.ndarray]) -> np.ndarray:
    """Get the tensor product of iterable operators."""
    gate = reduce(np.kron, operators)
    return gate


def make_gate(gates: dict[int, np.ndarray], n_bits: int) -> np.ndarray:
    """
    Constructs a n-quibit gate with specific operations on certain bits and the identity on others.

    gates: Dictionary mapping from bit index to the operation on that bit.
    """
    operators = (gates[i] if i in gates else np.eye(2) for i in range(n_bits))
    return tensor_product(operators)
    

def get_x(target: int, n_bits: int) -> np.ndarray:
    """Get Pauli X gate."""
    gates = {target: X_1}
    return make_gate(gates, n_bits)


def get_y(target: int, n_bits: int) -> np.ndarray:
    """Get Pauli Y gate."""
    gates = {target: Y_1}
    return make_gate(gates, n_bits)


def get_z(target: int, n_bits: int) -> np.ndarray:
    """Get Pauli Z gate."""
    gates = {target: Z_1}
    return make_gate(gates, n_bits)


def get_hadamard(target: int, n_bits: int) -> np.ndarray:
    """Get hadamard (H) gate"""
    gates = {target: H_1}
    return make_gate(gates, n_bits)


def get_s(target: int, n_bits: int) -> np.ndarray:
    """Get phase (P or S) gate"""
    gates = {target: S_1}
    return make_gate(gates, n_bits)


def get_t(target: int, n_bits: int) -> np.ndarray:
    """Get pi/8 (T) gate."""
    gates = {target: T_1}
    return make_gate(gates, n_bits)


def get_cnot(target: int, control: int, n_bits: int) -> np.ndarray:
    """Get controlled NOT (CNOT) gate."""
    id_term_gates = {
        control: OUTER_0_0,
        target: I_1,
    }
    id_term = make_gate(id_term_gates, n_bits)

    not_term_gates = {
        control: OUTER_1_1,
        target: X_1,
    }
    not_term = make_gate(not_term_gates, n_bits)

    return id_term + not_term


def get_cz(target: int, control: int, n_bits: int) -> np.ndarray:
    """Get controlled Pauli Z (CZ) gate."""
    id_term_gates = {
        control: np.array([[1., 0.], [0., 0.]]),
        target: I_1,
    }
    id_term = make_gate(id_term_gates, n_bits)

    z_term_gates = {
        control: np.array([[0., 0.], [0., 1.]]),
        target: Z_1,
    }
    z_term = make_gate(z_term_gates, n_bits)

    return id_term + z_term


def get_swap(i: int, j: int, n_bits: int) -> np.ndarray:
    """Get swap gate."""
    terms = []
    for pauli in [I_1, X_1, Y_1, Z_1]:
        term_gates = {
            i: pauli,
            j: pauli,
        }
        term_gate = make_gate(term_gates, n_bits)
        terms.append(term_gate)
    
    return np.sum(terms, axis=0) / 2


def get_ccnot(target: int, c1: int, c2: int, n_bits: int) -> np.ndarray:
    """Gets Toffoli (CCNOT) gate."""
    result = make_gate({
        c1: OUTER_0_0,
        c2: OUTER_0_0,
    }, n_bits)

    result += make_gate({
        c1: OUTER_0_0,
        c2: OUTER_1_1,
    }, n_bits)

    result += make_gate({
        c1: OUTER_1_1,
        c2: OUTER_0_0,
    }, n_bits)

    result += make_gate({
        c1: OUTER_1_1,
        c2: OUTER_1_1,
        target: X_1,
    }, n_bits)

    return result


def get_oracle_gate(
    n_bits: int,
    key: int | None = None,
    state: np.ndarray | None = None,
) -> np.ndarray:
    if (key is None) == (state is None):
        raise ValueError('Please assign only one of key or state')
    
    gate = np.eye(2**n_bits, dtype=complex)
    if key is not None:
        gate[key, key] = -1
    else:
        gate -= 2 * np.outer(state, state)

    return gate
