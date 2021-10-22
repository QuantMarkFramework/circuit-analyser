import typing
from pytket.routing import Architecture
import math


def diamonds(qubits: int, aslist: bool = False):
	"""
	Creates an architecture where the connections create diamonds in an 2
	dimensiona larray. There are always n * n diamonds so that there are enough
	qubits.

	This is similar to the architectuer used on Googles Sycamore processor. 
	"""
	connections: typing.List[typing.Tuple[int, int]] = []
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

	if aslist:
		return connections

	return Architecture(connections)
