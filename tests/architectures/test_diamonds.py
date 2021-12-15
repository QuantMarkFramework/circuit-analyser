import unittest
from analyser.architectures import diamonds


class TestDiamonds(unittest.TestCase):
	def test_1_qubit(self):
		correct = [(1, 0), (2, 0), (3, 1), (3, 2)]
		self.assertEqual(sorted(diamonds(1, aslist=True)), sorted(correct))

	def test_10_qubits(self):
		l1 = [(2, 0), (3, 0), (3, 1), (4, 1)]
		l2 = [(5, 2), (5, 3), (6, 3), (6, 4)]
		l3 = [(7, 5), (8, 5), (8, 6), (9, 6)]
		l4 = [(10, 7), (10, 8), (11, 8), (11, 9)]
		correct = [*l1, *l2, *l3, *l4]
		self.assertEqual(sorted(diamonds(10, aslist=True)), sorted(correct))

	def test_20_qubits(self):
		l1 = [(3, 0), (4, 0), (4, 1), (5, 1), (5, 2), (6, 2)]
		l2 = [(7, 3), (7, 4), (8, 4), (8, 5), (9, 5), (9, 6)]
		l3 = [(10, 7), (11, 7), (11, 8), (12, 8), (12, 9), (13, 9)]
		l4 = [(14, 10), (14, 11), (15, 11), (15, 12), (16, 12), (16, 13)]
		l5 = [(17, 14), (18, 14), (18, 15), (19, 15), (19, 16), (20, 16)]
		l6 = [(21, 17), (21, 18), (22, 18), (22, 19), (23, 19), (23, 20)]
		correct = [*l1, *l2, *l3, *l4, *l5, *l6]
		self.assertEqual(sorted(diamonds(20, aslist=True)), sorted(correct))

	def test_n_as_parameter(self):
		l1 = [(2, 0), (3, 0), (3, 1), (4, 1)]
		l2 = [(5, 2), (5, 3), (6, 3), (6, 4)]
		l3 = [(7, 5), (8, 5), (8, 6), (9, 6)]
		l4 = [(10, 7), (10, 8), (11, 8), (11, 9)]
		correct = [*l1, *l2, *l3, *l4]
		self.assertEqual(sorted(diamonds(n=2, aslist=True)), sorted(correct))
