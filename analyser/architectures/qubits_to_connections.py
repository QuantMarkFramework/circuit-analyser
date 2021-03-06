import typing


def qubits_to_connections(
	original: typing.List[typing.List[int]],
	qubits_per_connections: int = 1,
	return_new: bool = False,
	*args,
	**kwargs
) -> typing.Union[
	typing.List[typing.List[int]],
	typing.Tuple[typing.List[typing.List[int]], typing.List[int]]
]:
	"""
	Adds qubits along all connections.
	"""
	if qubits_per_connections < 1:
		raise TypeError("qubits_per_connections needs to be a integer that is 1 or bigger.")

	max_node = float("-inf")
	for connection in original:
		for node in connection:
			if node > max_node:
				max_node = node

	new_node = max_node + 1
	connections: typing.List[typing.List[int]] = []
	for connection in original:
		connections.append([connection[0], new_node])
		for _ in range(1, qubits_per_connections):
			new_node += 1
			connections.append([new_node - 1, new_node])
		connections.append([new_node, connection[1]])
		new_node += 1

	if return_new:
		return (connections, list(range(max_node + 1, new_node)))

	return connections
