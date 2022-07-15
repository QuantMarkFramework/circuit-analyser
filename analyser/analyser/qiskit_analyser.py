from analyser.analyser.analyser import Analyser
from analyser.architectures.two_directional import two_directional
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler import CouplingMap


class QiskitAnalyzer(Analyser):
	def __init__(self, routing_method=None, optimization_level=3):
		self.routing_method = routing_method
		self.optimization_level = optimization_level
		self.basis_gates = ["u1", "u2", "u3", "cx"]

	def _get_gate_count(self, circuit: QuantumCircuit):
		return circuit.count_ops()["cx"]

	def _get_gate_depth(self, circuit: QuantumCircuit):
		return circuit.depth(lambda i: i.operation.name == "cx")

	def _pre_routing_optimization(self, circuit: QuantumCircuit):
		pass_manager = generate_preset_pass_manager(
			self.optimization_level,
			basis_gates=self.basis_gates
		)
		return pass_manager.run(circuit)

	def _routing(self, circuit: QuantumCircuit, architecture):
		coupling_map = CouplingMap(two_directional(architecture))
		pass_manager = generate_preset_pass_manager(
			self.optimization_level,
			basis_gates=self.basis_gates,
			routing_method=self.routing_method,
			coupling_map=coupling_map
		)
		return pass_manager.run(circuit)

	def _post_routing_optimization(self, circuit):
		return circuit

# basis_gates, coupling_mao
