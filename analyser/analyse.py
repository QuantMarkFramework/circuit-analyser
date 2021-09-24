from analyser.CircuitAnalytics import CircuitAnalytics
from dataclasses import dataclass
import typing
import tequila as tq
from analyser.translate import tequila_to_tket
from pytket.routing import Architecture
from pytket.passes import DefaultMappingPass, RebaseTket, SequencePass, RepeatPass
from pytket.predicates import CompilationUnit
from pytket.circuit import OpType
from functools import reduce
import random
import numpy as np


@dataclass
class Result:
	gate_depth: int
	gate_count: int
	parameter_count: int


def cx_counter(count, gate):
	if gate.op.type == OpType.CX:
		return count + 1
	return count


def analyse(
	circuit: tq.QCircuit,
	architecture: Architecture = None,
	give_values: bool = False,
	runs: int = 1
):
	results: typing.List[Result] = []
	if not give_values:
		tket_circuit = tequila_to_tket(circuit, compile=True)
	if architecture:
		seqpass = SequencePass([
			DefaultMappingPass(architecture),
			RebaseTket(architecture)
		])
	else:
		seqpass = SequencePass([
			RebaseTket()
		])
	reppass = RepeatPass(seqpass)
	for _ in range(runs):
		if give_values:
			variables = {v: random.uniform(0, 2 * np.pi) for v in circuit.extract_variables()}
			tket_circuit = tequila_to_tket(circuit, variables, compile=True)
		cu = CompilationUnit(tket_circuit)
		reppass.apply(cu)
		outcome = cu.circuit
		results.append(Result(
			gate_depth=outcome.depth_by_type(OpType.CX),
			gate_count=reduce(cx_counter, outcome, 0),
			parameter_count=len(list(circuit.make_parameter_map().keys())),
		))
	return CircuitAnalytics(results)
