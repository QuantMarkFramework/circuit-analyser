import typing
from pytket.routing import Architecture
import math


def square_grid(qubits: int = 0, n: int = 0, aslist: bool = False):
	"""
	Creates a n * n square grid with enough qubits. You can give qubit count or
	n as a parameter.
	"""
	if qubits and n:
		raise ValueError("Must give either qubits count or n. Not both.")
	if not qubits and not n:
		raise ValueError("Must give either qubits count or n.")
	if qubits:
		n = math.ceil(math.sqrt(qubits))
	connections: typing.List[typing.Tuple[int, int]] = []

	for i in range(n - 1):
		connections.append((i, i + 1))
	for row in range(1, n):
		offset: int = row * n
		for i in range(n - 1):
			connections.append((offset + i, offset + i + 1))
			connections.append((offset + i - n, offset + i))
		connections.append((offset - 1, offset + n - 1))

	if aslist:
		return connections

	return Architecture(connections)
