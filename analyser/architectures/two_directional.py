import typing


def two_directional(connections: typing.List[typing.List[int]]):
	reverse = []
	for connection in connections:
		reverse.append([connection[1], connection[0]])
	return [*connections, *reverse]
