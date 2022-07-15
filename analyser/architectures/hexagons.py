import typing
from analyser.architectures._common_parts import test_input
import math


def hexagons(
	qubits: int = 0,
	n: int = 0,
	*args,
	**kwargs
) -> typing.List[typing.List[int]]:
	"""
	Creates a 2d grid with n * n hexagons that have.
	n is selected so that there are enough qubits. You can give qubit count or n
	as a parameter.

	This is similar to the heavy-hex architecture that is used by IBM, but does
	not have extrea qubits on the hexagon sides.
	"""
	test_input(qubits, n)
	connections: typing.List[typing.List[int]] = []
	if qubits:
		n: int = math.ceil(-1 + math.sqrt(1 + qubits / 2))

	if not qubits:
		qubits = 2 * n ** 2 + 4 * n

	_qubits = 2 * n ** 2 + 4 * n

	# horizontal
	for i in range(_qubits - 1):
		if ((i - 2 * n) % (2 * n + 2)):
			connections.append([i, i + 1])

	# vertical
	increment = 2 * n + 2
	if (n == 1):
		increment = 3
	for i in range(int((_qubits - increment) / 2) + 1):
		first = i * 2
		if ((i % (2 * n + 2)) >= n + 1):
			first -= 1
		# in some cases last row is "missing" first element
		if ((n > 1) and (n % 2) and ((first + increment) == (_qubits - (2 * n)))):
			increment -= 1
		connections.append([first, first + increment])

	return connections
