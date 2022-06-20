import unittest
from analyser.architectures import stack


class TestStack(unittest.TestCase):
	def test_1_layer(self):
		con = [(0, 1), (1, 2), (2, 3), (3, 0)]
		self.assertEqual(sorted(stack(con, 1, aslist=True)), sorted(con))

	def test_2_layers(self):
		l1 = [(0, 1), (1, 2), (2, 3), (3, 0)]
		l2 = [(4, 5), (5, 6), (6, 7), (7, 4)]
		l1_2 = [(0, 4), (1, 5), (2, 6), (3, 7)]
		con = [*l1, *l2, *l1_2]
		self.assertEqual(sorted(stack(l1, 2, aslist=True)), sorted(con))

	def test_3_layers(self):
		l1 = [(0, 1), (1, 2), (2, 3), (3, 0)]
		l2 = [(4, 5), (5, 6), (6, 7), (7, 4)]
		l3 = [(8, 9), (9, 10), (10, 11), (11, 8)]
		l1_2 = [(0, 4), (1, 5), (2, 6), (3, 7)]
		l2_3 = [(4, 8), (5, 9), (6, 10), (7, 11)]
		con = [*l1, *l2, *l3, *l1_2, *l2_3]
		self.assertEqual(sorted(stack(l1, 3, aslist=True)), sorted(con))

	def test_only_some_connections(self):
		l1 = [(0, 1), (1, 2), (2, 3), (3, 0)]
		l2 = [(4, 5), (5, 6), (6, 7), (7, 4)]
		l1_2 = [(1, 5), (3, 7)]
		con = [*l1, *l2, *l1_2]
		self.assertEqual(
			sorted(stack(l1, 2, [1, 3], aslist=True)),
			sorted(con)
		)
