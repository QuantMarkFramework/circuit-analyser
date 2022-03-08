import unittest
from analyser.extra import random_CX_H_T_circuit
from analyser import analyse
from analyser.architectures import big_hexagons, circle, diamonds, linear, octagons, square_grid
from analyser.architectures import fully_connected
import random
random.seed(1)


class TestAnalyse(unittest.TestCase):
	def test_architecture_comparison_with_seed(self):
		random.seed(1)
		circ = random_CX_H_T_circuit(qubits=10, cnots=100)
		arcf = [fully_connected, big_hexagons, circle, diamonds, linear, octagons, square_grid]
		arcs = [af(10) for af in arcf]
		res = analyse(
			circ,
			architecture=arcs,
			placement_type="linear",
		)
		results = [(r.gate_depth, r.gate_count) for r in res]
		goal = [(45, 93), (301, 573), (206, 408), (175, 252), (267, 528), (228, 423), (175, 297)]
		self.assertListEqual(results, goal)
