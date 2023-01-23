from analyser.analyser.analyser import Analyser
from qiskit import QuantumCircuit
from analyser.extra import dummy_router


class DummyAnalyser(Analyser):
	def __init__(self, ignore_errors=False):
		super().__init__(ignore_errors=ignore_errors)

	def _get_gate_count(self, circuit: QuantumCircuit):
		return circuit.count_ops()["cx"]

	def _get_gate_depth(self, circuit: QuantumCircuit):
		return circuit.depth(lambda i: i.operation.name == "cx")

	def _pre_routing_optimization(self, circuit: QuantumCircuit):
		return circuit

	def _routing(self, circuit: QuantumCircuit, architecture):
		return dummy_router(circuit, architecture)

	def _post_routing_optimization(self, circuit):
		return circuit
