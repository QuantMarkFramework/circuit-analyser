from random import randrange


def random_CX_H_T_circuit(qubits: int, cnots: int, library: str = "pytket"):
	"""
	Creates a circuit with random CNOTS that have a T or H before effected
	qubits.

	Uses random module for randomization.

	Library options are "pytket" and "qiskit"
	"""
	if not isinstance(library, str):
		raise ValueError("Library parameter has to be a string")
	elif library.lower() == "pytket":
		return _tket_version(qubits, cnots)
	elif library.lower() == "qiskit":
		return _qiskit_version(qubits, cnots)
	else:
		raise ValueError("Library has to be given as 'pytket' or 'qiskit'.")


PYTKET = True
try:
	from pytket import Circuit
except ImportError:
	PYTKET = False


def _tket_version(qubits: int, cnots: int):
	if not PYTKET:
		raise ImportError("Pytket installation not found.")
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


QISKIT = True
try:
	from qiskit import QuantumCircuit
except ImportError:
	QISKIT = False


def _qiskit_version(qubits: int, cnots: int):
	if not QISKIT:
		raise ImportError("Qiskit installation not found.")
	circuit: QuantumCircuit = QuantumCircuit(qubits)
	for _ in range(cnots):
		target: int = randrange(0, qubits)
		control: int = randrange(0, qubits - 1)
		if control >= target:
			control += 1
		circuit.t(target) if randrange(0, 2) else circuit.h(target)
		circuit.t(control) if randrange(0, 2) else circuit.h(control)
		circuit.cx(control_qubit=control, target_qubit=target)

	return circuit
