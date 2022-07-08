import typing
from pytket.architecture import Architecture


def stack(
	layer: typing.List[typing.Tuple[int, int]],
	height: int,
	connection_nodes: typing.List[int] = [],
	qubits_on_connections: int = 0,
	aslist: bool = False,
	*args,
	**kwargs
) -> typing.Union[Architecture, typing.List[typing.Tuple[int, int]]]:
	"""
	Stacks a architecture.
	"""
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

	if connection_nodes:
		node_set = set(connection_nodes)

	offset += len(node_set) * qubits_on_connections

	connections: typing.List[typing.Tuple[int, int]] = layer.copy()
	for level in range(1, height):
		for connection in layer:
			connections.append((
				connection[0] + (level * offset),
				connection[1] + (level * offset)
			))

		if qubits_on_connections:
			new_node = (offset * (level - 1)) + max_node + 1
			for node in node_set:
				connections.append((node + ((level - 1) * offset), new_node))
				for _ in range(1, qubits_on_connections):
					new_node += 1
					connections.append((new_node - 1, new_node))
				connections.append((new_node, node + (level * offset)))
				new_node += 1
		else:
			for node in node_set:
				connections.append((
					node + ((level - 1) * offset),
					node + (level * offset)
				))

	if aslist:
		return connections

	return Architecture(connections)
