from random import randrange
from pytket import Circuit


def random_CX_H_T_circuit(qubits: int, cnots: int) -> Circuit:
	"""
	Creates a circuit with random CNOTS that have a T or H before effected
	qubits.

	Uses random module for randomization.
	"""
	circuit: Circuit = Circuit(qubits)
	for _ in range(cnots):
		target: int = randrange(0, qubits)
		control: int = randrange(0, qubits - 1)
		if control >= target:
			control += 1
		circuit.T(target) if randrange(0, 2) else circuit.H(target)
		circuit.T(control) if randrange(0, 2) else circuit.H(control)
		circuit.CX(control_qubit=control, target_qubit=target)

	return circuit
