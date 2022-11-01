import typing


def minimum_viable(generator, qubits: int) -> typing.List[typing.List[int]]:
	for n in range(1, qubits + 1):
		proposal = generator(n=n)
		prop_q = len({qubit for connection in proposal for qubit in connection})
		if prop_q >= qubits:
			return proposal
	return False
