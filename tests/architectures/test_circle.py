import unittest
from analyser.architectures import circle


class TestCircle(unittest.TestCase):
	def test_3_qubits(self):
		correct = [(0, 1), (1, 2), (0, 2)]
		self.assertEqual(sorted(circle(3, aslist=True)), sorted(correct))

	def test_7_qubits(self):
		correct = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (0, 6)]
		self.assertEqual(sorted(circle(7, aslist=True)), sorted(correct))
