import typing
from pytket.routing import Architecture
from analyser.architectures import linear


def circle(qubits: int, aslist: bool = False, *args, **kwargs):
	connections: typing.List[typing.Tuple[int, int]]
	connections = linear(qubits, True)
	connections.append((0, qubits - 1))

	if aslist:
		return connections

	return Architecture(connections)
