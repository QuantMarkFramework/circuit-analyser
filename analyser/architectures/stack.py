import typing
from pytket.routing import Architecture


def stack(
	layer: typing.List[typing.Tuple[int, int]],
	height: int,
	aslist: bool = False,
	*args,
	**kwargs
) -> typing.Union[Architecture, typing.List[typing.Tuple[int, int]]]:
	"""
	Stacks a architecture.
	"""
	if not layer:
		raise TypeError("Layer needs to have connections.")

	min_node = float("inf")
	max_node = float("-inf")
	node_set = set(())
	for connection in layer:
		for node in connection:
			node_set.add(node)
			if node < min_node:
				min_node = node
			if node > max_node:
				max_node = node
	offset = max_node - min_node + 1

	connections: typing.List[typing.Tuple[int, int]] = layer.copy()
	for level in range(1, height):
		for connection in layer:
			connections.append((
				connection[0] + (level * offset),
				connection[1] + (level * offset)
			))

		for node in node_set:
			connections.append((
				node + ((level - 1) * offset),
				node + (level * offset)
			))

	if aslist:
		return connections

	return Architecture(connections)
