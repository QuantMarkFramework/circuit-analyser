import typing


def test_input(qubits: int, n: int):
	if qubits and n:
		raise ValueError("Must give either qubits count or n. Not both.")
	if not qubits and not n:
		raise ValueError("Must give either qubits count or n.")


def exact_qubit_count(count: int, connections: typing.List[typing.List[int]]):
	return [con for con in connections if con[0] < count and con[1] < count]
