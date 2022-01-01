from random import randrange
import tequila as tq
from tequila.circuit.circuit import QCircuit


def random_CX_H_T_circuit(qubits: int, cnots: int) -> QCircuit:
	"""
	Creates a circuit with random cnots that have a T or H before effected
	qubits.

	Uses random module for randomization.
	"""
	circuit: QCircuit = QCircuit()
	for _ in range(cnots):
		target: int = randrange(0, qubits)
		control: int = randrange(0, qubits - 1)
		circuit += tq.gates.T(target) if randrange(0, 2) else tq.gates.H(target)
		circuit += tq.gates.T(control) if randrange(0, 2) else tq.gates.H(control)
		if control >= target:
			control += 1
		circuit += tq.gates.CX(control=control, target=target)

	return circuit
