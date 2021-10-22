import unittest
from analyser.architectures import linear


class TestLinear(unittest.TestCase):
	def test_3_qubits(self):
		correct = [(0, 1), (1, 2)]
		self.assertEqual(sorted(linear(3, True)), sorted(correct))

	def test_7_qubits(self):
		correct = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
		self.assertEqual(sorted(linear(7, True)), sorted(correct))
