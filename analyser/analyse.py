from dataclasses import dataclass
from pytket.routing import Architecture, GraphPlacement, LinePlacement
from pytket.passes import FullPeepholeOptimise, RebaseTket, RoutingPass, PlacementPass
from pytket.passes import SequencePass, DecomposeBoxes, DelayMeasures, RemoveRedundancies
from pytket.predicates import CompilationUnit, GateSetPredicate, ConnectivityPredicate
from pytket.predicates import NoMidMeasurePredicate
from pytket.circuit import OpType
from functools import reduce
import typing

HAS_TEQUILA = True
try:
	import tequila as tq
	from analyser.translate import tequila_to_tket
except ImportError:
	HAS_TEQUILA = False


class AnalyseError(Exception):
	pass


@dataclass
class CircuitAnalytics:
	qubit_count: int
	gate_depth: int
	gate_count: int


def cx_counter(count, gate):
	if gate.op.type == OpType.CX:
		return count + 1
	return count


def create_pass(
	architecture: Architecture = None,
	placement_type: str = "graph",
	graph_placement_timeout: int = 120000,
):
	"""
	placement options "graph" "linear"
	"""
	passes = [DecomposeBoxes(), RebaseTket(), FullPeepholeOptimise()]

	if architecture:
		if not isinstance(placement_type, str):
			raise ValueError("placement has to be given as 'graph' or 'linear'.")
		elif placement_type.lower() == "graph":
			placement = GraphPlacement(architecture)
			placement.modify_config(timeout=graph_placement_timeout)
		elif placement_type.lower() == "linear":
			placement = LinePlacement(architecture)
		else:
			raise ValueError("placement has to be given as 'graph' or 'linear'.")
		passes.append(PlacementPass(placement))
		passes.append(RoutingPass(architecture))

	passes.append(DelayMeasures())
	passes.append(RebaseTket())
	passes.append(RemoveRedundancies())

	return SequencePass(passes)


def analyse(
	circuit,
	architecture: typing.Union[Architecture, typing.List[Architecture]] = None,
	placement_type: str = "graph",
	graph_placement_timeout: int = 120000,
):
	if HAS_TEQUILA and isinstance(circuit, tq.QCircuit):
		circuit = tequila_to_tket(circuit, compile=True)
	cu = CompilationUnit(circuit)
	create_pass(
		architecture=architecture,
		placement_type=placement_type,
		graph_placement_timeout=graph_placement_timeout
	).apply(cu)
	outcome = cu.circuit
	if not GateSetPredicate({OpType.CX, OpType.TK1}).verify(outcome):
		raise AnalyseError("Resulting circuit has wrong gates. Most likely not a user error.")
	if architecture and not ConnectivityPredicate(architecture).verify(outcome):
		raise AnalyseError("Resulting circuit has wrong gates. Most likely not a user error.")
	if not NoMidMeasurePredicate().verify(outcome):
		raise AnalyseError("Resulting circuit has mid measures. Most likely not a user error.")
	return CircuitAnalytics(
		qubit_count=outcome.n_qubits,
		gate_depth=outcome.depth_by_type(OpType.CX),
		gate_count=reduce(cx_counter, outcome, 0)
	)
