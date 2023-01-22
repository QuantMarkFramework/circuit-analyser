from abc import ABC, abstractmethod
from dataclasses import dataclass
import time


@dataclass
class CircuitAnalytics:
	gate_count: int
	gate_depth: int
	transpile_time: int


class Analyser(ABC):
	def __init__(self, ignore_errors=False):
		self.ignore_errors = ignore_errors

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

	def _routing_and_measuring(self, circuit, architecture, pre_time):
		complete_time = pre_time
		if architecture:
			if self.ignore_errors:
				try:
					start_time = time.time()
					circuit = self._routing(circuit, architecture)
					complete_time += time.time() - start_time
				except Exception:
					return CircuitAnalytics(None, None, None)
			else:
				start_time = time.time()
				circuit = self._routing(circuit, architecture)
				complete_time += time.time() - start_time

		if self.ignore_errors:
			try:
				start_time = time.time()
				circuit = self._post_routing_optimization(circuit)
				complete_time += time.time() - start_time
			except Exception:
				return CircuitAnalytics(None, None, None)
		else:
			start_time = time.time()
			circuit = self._post_routing_optimization(circuit)
			complete_time += time.time() - start_time

		return CircuitAnalytics(
			gate_count=self._get_gate_count(circuit),
			gate_depth=self._get_gate_depth(circuit),
			transpile_time=complete_time
		)

	def analyse(self, circuit, architecture) -> CircuitAnalytics:
		pre_time = 0
		if self.ignore_errors:
			try:
				start_time = time.time()
				circuit = self._pre_routing_optimization(circuit)
				pre_time = time.time() - start_time
			except Exception:
				if isinstance(architecture, list):
					return [CircuitAnalytics(None, None, None) for _ in architecture]
				return CircuitAnalytics(None, None, None)
		else:
			start_time = time.time()
			circuit = self._pre_routing_optimization(circuit)
			pre_time = time.time() - start_time

		if isinstance(architecture, list):
			return [
				self._routing_and_measuring(circuit.copy(), arc, pre_time)
				for arc in architecture
			]

		return self._routing_and_measuring(circuit, architecture, pre_time)
