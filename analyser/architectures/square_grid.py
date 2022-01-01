import typing
from pytket.routing import Architecture
from analyser.architectures._common_parts import test_input, exact_qubit_count
import math


def square_grid(
	qubits: int = 0,
	n: int = 0,
	aslist: bool = False,
	exact: bool = False,
	*args,
	**kwargs
) -> Architecture:
	"""
	Creates a n * n square grid with enough qubits. You can give qubit count or
	n as a parameter.

	When exact is used, qubits are removed from one side, till the exact qubit
	count is achieved.
	"""
	test_input(qubits, n, exact)
	connections: typing.List[typing.Tuple[int, int]] = []
	if qubits:
		n = math.ceil(math.sqrt(qubits))

	for i in range(n - 1):
		connections.append((i, i + 1))
	for row in range(1, n):
		offset: int = row * n
		for i in range(n - 1):
			connections.append((offset + i, offset + i + 1))
			connections.append((offset + i - n, offset + i))
		connections.append((offset - 1, offset + n - 1))

	if exact:
		connections = exact_qubit_count(qubits, connections)

	if aslist:
		return connections

	return Architecture(connections)
