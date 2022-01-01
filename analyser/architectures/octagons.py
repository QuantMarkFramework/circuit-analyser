import typing
from pytket.routing import Architecture
from analyser.architectures._common_parts import test_input, exact_qubit_count
import math


class Octagon:
	def __init__(self, identifier: int) -> None:
		self.offset: int = identifier * 8
		self.connections: typing.List[typing.Tuple[int, int]] = []
		for i in range(7):
			self.connections.append((i + self.offset, i + 1 + self.offset))
		self.connections.append((7 + self.offset, self.offset))

	def top(self) -> typing.Tuple[int, int]:
		return (self.offset, 1 + self.offset)

	def right(self) -> typing.Tuple[int, int]:
		return (2 + self.offset, 3 + self.offset)

	def bottom(self) -> typing.Tuple[int, int]:
		return (4 + self.offset, 5 + self.offset)

	def left(self) -> typing.Tuple[int, int]:
		return (6 + self.offset, 7 + self.offset)


class SideStartOctagon(Octagon):
	def left(self) -> typing.Tuple[int, int]:
		return (self.offset, 1 + self.offset)

	def top(self) -> typing.Tuple[int, int]:
		return (2 + self.offset, 3 + self.offset)

	def right(self) -> typing.Tuple[int, int]:
		return (4 + self.offset, 5 + self.offset)

	def bottom(self) -> typing.Tuple[int, int]:
		return (6 + self.offset, 7 + self.offset)


def octagons(
	qubits: int = 0,
	n: int = 0,
	aslist: bool = False,
	exact: bool = False,
	*args,
	**kwargs
) -> Architecture:
	"""
	Creates octagons (like in Rigettis Apen-9) and connects them in a 2
	dimensional grit. There are always n x n octagons, where n^2 * 8 is greater
	than the given qubit count. You can give qubit count or n as a parameter.

	When exact is used, qubits are removed from one side, till the exact qubit
	count is achieved.
	"""
	test_input(qubits, n, exact)
	connections: typing.List[typing.Tuple[int, int]] = []
	if qubits:
		n = math.ceil(math.sqrt(math.ceil(qubits / 8)))
	identifier = 0
	octagons: typing.List[typing.List[Octagon]] = []
	octagon_class = SideStartOctagon if exact and qubits > 8 and qubits < 16 else Octagon

	for _ in range(n):
		row = []
		for _ in range(n):
			octagon = octagon_class(identifier)
			connections.extend(octagon.connections)
			row.append(octagon)
			identifier += 1
		octagons.append(row)

	for y in range(n):
		for x in range(n - 1):
			right1, right2 = octagons[y][x].right()
			left2, left1 = octagons[y][x + 1].left()
			connections.extend([(right1, left1), (right2, left2)])

	for x in range(n):
		for y in range(n - 1):
			bottom1, bottom2 = octagons[y][x].bottom()
			top2, top1 = octagons[y + 1][x].top()
			connections.extend([(bottom1, top1), (bottom2, top2)])

	if exact:
		connections = exact_qubit_count(qubits, connections)

	if aslist:
		return connections

	return Architecture(connections)
