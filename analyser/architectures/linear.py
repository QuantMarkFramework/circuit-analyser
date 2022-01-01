import typing
from pytket.routing import Architecture


def linear(qubits: int, aslist: bool = False, *args, **kwargs):
	connections: typing.List[typing.Tuple[int, int]] = []
	for i in range(qubits - 1):
		connections.append((i, i + 1))

	if aslist:
		return connections

	return Architecture(connections)
