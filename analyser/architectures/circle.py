import typing
from analyser.architectures import linear


def circle(qubits: int, *args, **kwargs) -> typing.List[typing.List[int]]:
	connections: typing.List[typing.List[int]]
	connections = linear(qubits, True)
	connections.append([0, qubits - 1])

	return connections
