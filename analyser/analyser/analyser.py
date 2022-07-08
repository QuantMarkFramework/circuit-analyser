from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CircuitAnalytics:
	gate_count: int
	gate_depth: int


class Analyser(ABC):

	@abstractmethod
	def _get_gate_count(self, circuit):
		pass

	@abstractmethod
	def _get_gate_depth(self, circuit):
		pass

	@abstractmethod
	def _pre_routing_optimization(self, circuit):
		pass

	@abstractmethod
	def _routing(self, circuit, architecture):
		pass

	@abstractmethod
	def _post_routing_optimization(self, circuit):
		pass

	def _routing_and_measuring(self, circuit, architecture):
		if architecture:
			circuit = self._routing(circuit, architecture)
		circuit = self._post_routing_optimization(circuit)

		return CircuitAnalytics(
			gate_count=self._get_gate_count(circuit),
			gate_depth=self._get_gate_depth(circuit),
		)

	def analyse(self, circuit, architecture) -> CircuitAnalytics:
		circuit = self._pre_routing_optimization(circuit)

		if isinstance(architecture, list):
			return [self._routing_and_measuring(circuit, arc) for arc in architecture]

		return self._routing_and_measuring(circuit, architecture)
