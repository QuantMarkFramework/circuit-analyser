import typing


class CircuitAnalytics:
	def __init__(self, results: typing.List[typing.Dict[str, int]]):
		self.results = results

	def __str__(self):
		return "\n".join([str(result) for result in self.results])
