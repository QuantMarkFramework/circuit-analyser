import unittest
from analyser.architectures import square_grid


class TestSquareGrid(unittest.TestCase):
	def test_1_qubit(self):
		empty = []
		self.assertEqual(sorted(square_grid(1, aslist=True)), sorted(empty))

	def test_3_qubits(self):
		con = [[0, 1], [2, 3], [0, 2], [1, 3]]
		self.assertEqual(sorted(square_grid(qubits=3, aslist=True)), sorted(con))

	def test_16_qubits(self):
		row12 = [[0, 1], [1, 2], [2, 3], [4, 5], [5, 6], [6, 7]]
		row23 = [[8, 9], [9, 10], [10, 11], [12, 13], [13, 14], [14, 15]]
		col12 = [[0, 4], [4, 8], [8, 12], [1, 5], [5, 9], [9, 13]]
		col34 = [[2, 6], [6, 10], [10, 14], [3, 7], [7, 11], [11, 15]]
		correct = [*row12, *row23, *col12, *col34]
		self.assertEqual(sorted(square_grid(16, aslist=True)), sorted(correct))

	def test_n_as_parameter(self):
		row12 = [[0, 1], [1, 2], [2, 3], [4, 5], [5, 6], [6, 7]]
		row23 = [[8, 9], [9, 10], [10, 11], [12, 13], [13, 14], [14, 15]]
		col12 = [[0, 4], [4, 8], [8, 12], [1, 5], [5, 9], [9, 13]]
		col34 = [[2, 6], [6, 10], [10, 14], [3, 7], [7, 11], [11, 15]]
		correct = [*row12, *row23, *col12, *col34]
		self.assertEqual(sorted(square_grid(n=3, aslist=True)), sorted(correct))
