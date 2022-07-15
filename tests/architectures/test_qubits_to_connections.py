import unittest
from analyser.architectures import qubits_to_connections


class TestQubitsToConnections(unittest.TestCase):
	def test_1_per_connection(self):
		con = [[0, 1], [1, 2], [2, 3], [3, 0]]
		cor = [[0, 4], [4, 1], [1, 5], [5, 2], [2, 6], [6, 3], [3, 7], [7, 0]]
		self.assertEqual(
			sorted(qubits_to_connections(con, 1, aslist=True)),
			sorted(cor)
		)

	def test_3_per_connections(self):
		con = [[0, 1], [1, 2]]
		cor = [[0, 3], [3, 4], [4, 5], [5, 1], [1, 6], [6, 7], [7, 8], [8, 2]]
		self.assertEqual(
			sorted(qubits_to_connections(con, 3, aslist=True)),
			sorted(cor)
		)

	def test_return_new(self):
		con = [[3, 1], [1, 5]]
		corr = [6, 7, 8, 9, 10, 11]
		new_qubits = qubits_to_connections(con, 3, return_new=True)[1]
		self.assertEqual(
			sorted(new_qubits),
			sorted(corr)
		)
