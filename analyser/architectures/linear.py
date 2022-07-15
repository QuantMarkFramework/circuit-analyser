import typing


def linear(qubits: int, *args, **kwargs) -> typing.List[typing.List[int]]:
	connections: typing.List[typing.List[int]] = []
	for i in range(qubits - 1):
		connections.append([i, i + 1])

	return connections
