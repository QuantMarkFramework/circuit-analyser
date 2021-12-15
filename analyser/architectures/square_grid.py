from pytket.routing import SquareGrid
import math


def square_grid(qubits: int = 0, n: int = 0):
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
	return SquareGrid(n, n)
