import unittest
from analyser.extra import random_CX_H_T_circuit
from pytket import Circuit
import random


class TestBigHexagons(unittest.TestCase):
	def test_with_seeded(self):
		random.seed(1)
		circ = random_CX_H_T_circuit(4, 5)
		goal = Circuit(4).T(0).H(1).T(2).T(3).CX(2, 0).CX(3, 1).T(0).H(1).H(2)
		goal.H(3).CX(0, 3).T(0).H(3).CX(2, 0).CX(1, 3)
		self.assertEqual(circ, goal)
