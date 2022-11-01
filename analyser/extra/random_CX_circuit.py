from random import randrange, random
from pytket import Circuit, OpType
from qiskit import QuantumCircuit
from numpy import pi


def random_CX_circuit(
	qubits: int,
	cnots: int,
	library: str,
	single_qubit_gates: bool = True
):
	if not isinstance(library, str):
		raise ValueError("Library parameter has to be a string")
	elif library.lower() == "pytket":
		return _tket_version(qubits, cnots, single_qubit_gates)
	elif library.lower() == "qiskit":
		return _qiskit_version(qubits, cnots, single_qubit_gates)
	else:
		raise ValueError("Library has to be given as 'pytket' or 'qiskit'.")


def _r(val: int):
	return val * random()


def _tket_version(qubits: int, cnots: int, single_qubit_gates: bool):
	circuit: Circuit = Circuit(qubits)
	for _ in range(cnots):
		target: int = randrange(0, qubits)
		control: int = randrange(0, qubits - 1)
		if control >= target:
			control += 1
		if single_qubit_gates:
			circuit.add_gate(OpType.U3, [_r(4), _r(4), _r(4)], [target])
			circuit.add_gate(OpType.U3, [_r(4), _r(4), _r(4)], [control])
		circuit.CX(control_qubit=control, target_qubit=target)
	return circuit


def _qiskit_version(qubits: int, cnots: int, single_qubit_gates: bool):
	circuit: QuantumCircuit = QuantumCircuit(qubits)
	for _ in range(cnots):
		target: int = randrange(0, qubits)
		control: int = randrange(0, qubits - 1)
		if control >= target:
			control += 1
		if single_qubit_gates:
			circuit.u(_r(4 * pi), _r(4 * pi), _r(4 * pi), target)
			circuit.u(_r(4 * pi), _r(4 * pi), _r(4 * pi), control)
		circuit.cx(control_qubit=control, target_qubit=target)
	return circuit
