# %%
from qiskit import QuantumCircuit
import networkx as nx
import operator
import warnings
from math import ceil, floor
warnings.filterwarnings("ignore", category=DeprecationWarning)


def dummy_router(
	circuit: QuantumCircuit,
	connections: list,
	two_way_approach: bool = True
):
	n_qubits = len(circuit.qubits)
	graph = nx.Graph(connections)
	n_real_qubits = len(graph.nodes())
	while (graph.number_of_nodes() > n_qubits):
		asdict = dict(nx.all_pairs_shortest_path_length(graph))
		sums = {k: sum(v.values()) for k, v in asdict.items()}
		out = max(sums.items(), key=operator.itemgetter(1))[0]
		graph.remove_node(out)
	inv_q_map = {i: node for i, node in enumerate(graph.nodes())}  # format "fake:real"
	new_circuit = QuantumCircuit(n_real_qubits)
	for instruction in list(circuit):
		if instruction.operation.num_qubits > 2:
			raise ValueError("Dummy compiler does not support gates with more than 2 qubits.")
		if instruction.operation.num_clbits > 0 or instruction.operation.num_qubits < 1:
			raise ValueError("Dummy compiler supports only qubit operations.")
		qubits = [qubit.index for qubit in instruction.qubits]
		if instruction.operation.num_qubits == 1:
			new_circuit.append(instruction.operation, [inv_q_map[qubits[0]]])
			continue

		qubit_map = {v: k for k, v in inv_q_map.items()}
		path = nx.shortest_path(graph, inv_q_map[qubits[0]], inv_q_map[qubits[1]])

		if two_way_approach:
			for i in range(ceil(len(path) / 2) - 1):
				_insert_swap(new_circuit, qubit_map, path[i], path[i + 1])

			for i in range(floor(len(path) / 2) - 1):
				_insert_swap(new_circuit, qubit_map, path[-1 - i], path[-2 - i])
		else:
			for i in range(len(path) - 2):
				_insert_swap(new_circuit, qubit_map, path[i], path[i + 1])

		inv_q_map = {v: k for k, v in qubit_map.items()}
		target_qubits = [inv_q_map[qubit] for qubit in qubits]
		new_circuit.append(instruction.operation, target_qubits)
	return new_circuit, {v: k for k, v in inv_q_map.items()}


def _insert_swap(new_circuit, qubit_map, q1, q2):
	new_circuit.cx(q1, q2)
	new_circuit.cx(q2, q1)
	new_circuit.cx(q1, q2)

	current_q_1 = qubit_map[q1]
	current_q_2 = qubit_map[q2]
	qubit_map[q1] = current_q_2
	qubit_map[q2] = current_q_1
