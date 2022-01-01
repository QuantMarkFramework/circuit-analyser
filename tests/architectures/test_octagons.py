import unittest
from analyser.architectures import octagons


class TestOctagons(unittest.TestCase):
	def test_7_qubits(self):
		oneOctagon = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)]
		self.assertEqual(sorted(octagons(7, aslist=True)), sorted(oneOctagon))

	def test_24_qubits(self):
		oct1 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)]
		oct2 = [(8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 8)]
		oct3 = [(16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23), (23, 16)]
		oct4 = [(24, 25), (25, 26), (26, 27), (27, 28), (28, 29), (29, 30), (30, 31), (31, 24)]
		con = [(2, 15), (3, 14), (18, 31), (19, 30), (5, 16), (4, 17), (13, 24), (12, 25)]
		correct = [*oct1, *oct2, *oct3, *oct4, *con]
		self.assertEqual(sorted(octagons(24, aslist=True)), sorted(correct))

	def test_n_as_parameter(self):
		oct1 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)]
		oct2 = [(8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 8)]
		oct3 = [(16, 17), (17, 18), (18, 19), (19, 20), (20, 21), (21, 22), (22, 23), (23, 16)]
		oct4 = [(24, 25), (25, 26), (26, 27), (27, 28), (28, 29), (29, 30), (30, 31), (31, 24)]
		con = [(2, 15), (3, 14), (18, 31), (19, 30), (5, 16), (4, 17), (13, 24), (12, 25)]
		correct = [*oct1, *oct2, *oct3, *oct4, *con]
		self.assertEqual(sorted(octagons(n=2, aslist=True)), sorted(correct))

	def test_exact_true(self):
		oct1 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)]
		oct2 = [(8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 8)]
		con = [(2, 15), (3, 14)]
		correct = [*oct1, *oct2, *con]
		self.assertEqual(sorted(octagons(16, aslist=True, exact=True)), sorted(correct))

	def test_exact_2_octagons_cornercase(self):
		oct1 = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)]
		oct2 = [(8, 9), (9, 10), (10, 11), (11, 12), (12, 13)]
		con = [(4, 9), (5, 8)]
		correct = [*oct1, *oct2, *con]
		self.assertEqual(sorted(octagons(14, aslist=True, exact=True)), sorted(correct))
