import typing
from analyser.architectures._common_parts import test_input
import math


def square_grid(
	qubits: int = 0,
	n: int = 0,
	*args,
	**kwargs
) -> typing.List[typing.List[int]]:
	"""
	Creates a n * n square grid with enough qubits. You can give qubit count or
	n as a parameter.

	When exact is used, qubits are removed from one side, till the exact qubit
	count is achieved.
	"""
	test_input(qubits, n)
	connections: typing.List[typing.List[int]] = []
	if qubits:
		n = math.ceil(math.sqrt(qubits) - 1)

	for i in range(n):
		connections.append([i, i + 1])
	for row in range(1, n + 1):
		offset: int = row * (n + 1)
		for i in range(n):
			connections.append([offset + i, offset + i + 1])
			connections.append([offset + i - n - 1, offset + i])
		connections.append([offset - 1, offset + n])

	return connections
