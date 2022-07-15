import typing
from analyser.architectures._common_parts import test_input
import math


def diamonds(
	qubits: int = 0,
	n: int = 0,
	*args,
	**kwargs
) -> typing.List[typing.List[int]]:
	"""
	Creates an architecture where the connections create diamonds in an 2
	dimensiona larray. There are always n * n diamonds so that there are enough
	qubits. You can give qubit count or n as a parameter.

	This is similar to the architectuer used on Googles Sycamore processor.
	"""
	test_input(qubits, n)
	connections: typing.List[typing.List[int]] = []
	if qubits:
		n = math.ceil((1 - math.sqrt(1 + 2 * qubits)) / -2)
	node = n
	for layer in range(2 * n):
		if not layer % 2:
			connections.append([node, node - n])
			node += 1
			for _ in range(n - 1):
				connections.append([node, node - n - 1])
				connections.append([node, node - n])
				node += 1
			connections.append([node, node - n - 1])
			node += 1
		else:
			for _ in range(n):
				connections.append([node, node - n - 1])
				connections.append([node, node - n])
				node += 1

	return connections
