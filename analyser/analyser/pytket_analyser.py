from functools import reduce
from analyser.analyser.analyser import Analyser


PYTKET = True
try:
	from pytket.circuit import OpType
	from pytket.predicates import CompilationUnit
	from pytket.passes import FullPeepholeOptimise, RebaseTket, RoutingPass, PlacementPass
	from pytket.passes import SequencePass, DecomposeBoxes, DelayMeasures, RemoveRedundancies
	from pytket.placement import GraphPlacement, LinePlacement
	from pytket.architecture import Architecture
except ImportError:
	PYTKET = False


def _cx_counter(count, gate):
	if gate.op.type == OpType.CX:
		return count + 1
	return count


class PytketAnalyzer(Analyser):
	def __init__(self, placement_type: str = "linear"):
		if not PYTKET:
			raise ImportError("Library 'pytket' is needed to use PytketAnalyzer.")

		if not isinstance(placement_type, str):
			raise ValueError("placement has to be given as 'graph' or 'linear'.")
		elif placement_type.lower() == "graph":
			self.placement = GraphPlacement
		elif placement_type.lower() == "linear":
			self.placement = LinePlacement
		else:
			raise ValueError("placement has to be given as 'graph' or 'linear'.")

		self.PRE_PASS = SequencePass([DecomposeBoxes(), RebaseTket(), FullPeepholeOptimise()])
		self.POST_PASS = SequencePass([DelayMeasures(), RebaseTket(), RemoveRedundancies()])

	def _get_gate_count(self, circuit):
		return reduce(_cx_counter, circuit, 0)

	def _get_gate_depth(self, circuit):
		return circuit.depth_by_type(OpType.CX)

	def _pre_routing_optimization(self, circuit):
		cu = CompilationUnit(circuit)
		self.PRE_PASS.apply(cu)
		return cu.circuit

	def _routing(self, circuit, architecture):
		architecture = Architecture(architecture)
		cu = CompilationUnit(circuit)
		SequencePass([PlacementPass(self.placement(architecture)), RoutingPass(architecture)]).apply(cu)
		return cu.circuit

	def _post_routing_optimization(self, circuit):
		cu = CompilationUnit(circuit)
		self.POST_PASS.apply(cu)
		return cu.circuit
