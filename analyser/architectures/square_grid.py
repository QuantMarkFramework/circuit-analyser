from pytket.routing import SquareGrid
import math


def square_grid(qubits: int):
	n = math.ceil(math.sqrt(qubits))
	return SquareGrid(n, n)
