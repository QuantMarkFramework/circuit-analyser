import typing
from pytket.routing import Architecture
from analyser.architectures._common_parts import test_input, exact_qubit_count
import math


def diamonds(
	qubits: int = 0,
	n: int = 0,
	aslist: bool = False,
	exact: bool = False,
	*args,
	**kwargs
) -> Architecture:
	"""
	Creates an architecture where the connections create diamonds in an 2
	dimensiona larray. There are always n * n diamonds so that there are enough
	qubits. You can give qubit count or n as a parameter.

	When exact is used, qubits are removed from one side, till the exact qubit
	count is achieved.

	This is similar to the architectuer used on Googles Sycamore processor.
	"""
	test_input(qubits, n, exact)
	connections: typing.List[typing.Tuple[int, int]] = []
	if qubits:
		n = math.ceil((1 - math.sqrt(1 + 2 * qubits)) / -2)
	node = n
	for layer in range(2 * n):
		if not layer % 2:
			connections.append((node, node - n))
			node += 1
			for _ in range(n - 1):
				connections.append((node, node - n - 1))
				connections.append((node, node - n))
				node += 1
			connections.append((node, node - n - 1))
			node += 1
		else:
			for _ in range(n):
				connections.append((node, node - n - 1))
				connections.append((node, node - n))
				node += 1

	if exact:
		connections = exact_qubit_count(qubits, connections)

	if aslist:
		return connections

	return Architecture(connections)
