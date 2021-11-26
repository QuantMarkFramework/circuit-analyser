import typing
from pytket.routing import Architecture
import math


def big_hexagons(qubits: int, aslist: bool = False):
	"""
	Creates a 2d grid with n * n hexagons that have 2 connection long sides.
	n is selected so that there are enough qubits.

	This is follows the heavy-hex architecture that is used by IBM.
	"""
	connections: typing.List[typing.Tuple[int, int]] = []
	n: int = math.ceil((-8 + math.sqrt(84 + (20 * qubits))) / 10)

	# first row and n first connections to second
	for i in range((4 * n)):
		connections.append((i, i + 1))
		if (i % 4) == 0:
			jump: int = (4 * n) + 1 + (i // 4)
			if n == 1:
				to: int = 7
			else:
				to: int = (5 * n) + 4 + i
			connections.append((i, jump))
			connections.append((jump, to))

	# last connection to second row
	last: int = 4 * n
	jump: int = (5 * n) + 1
	if n == 1:
		to: int = 11
	else:
		to: int = (9 * n) + 4
	connections.append((last, jump))
	connections.append((jump, to))

	# Middle rows and connections to next
	for row in range(n - 1):
		start: int = ((5 * n) * (row + 1)) + (4 * row) + 2
		for i in range((4 * n) + 2):
			connections.append((start + i, start + i + 1))
			if (((i - (2 * (row % 2))) % 4) == 0):
				jump: int = start + (4 * n) + 3 + ((i - (2 * (row % 2))) // 4)
				to: int = start + (5 * n) + 4 + (i - (2 * (row % 2)))
				connections.append((start + i, jump))
				connections.append((jump, to))
		# Last connection on some rows
		if (row % 2):
			i = (4 * n) + 2
			jump: int = start + (4 * n) + 3 + ((i - (2 * (row % 2))) // 4)
			to: int = start + (5 * n) + 4 + (i - (2 * (row % 2)))
			connections.append((start + i, jump))
			connections.append((jump, to))

	# Last Row
	last_start: int = ((5 * n) * n) + (4 * n) - 2
	for i in range((4 * n)):
		connections.append((last_start + i, last_start + i + 1))
	if aslist:
		return connections

	return Architecture(connections)
