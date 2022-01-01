from pytket.routing import FullyConnected


def fully_connected(qubits: int, *args, **kwargs):
	return FullyConnected(qubits)
