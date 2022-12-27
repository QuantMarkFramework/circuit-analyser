# %%
from qiskit import QuantumCircuit
import networkx as nx
import operator
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def dummy_router(circuit: QuantumCircuit, connections: list):
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
		for i in range(len(path) - 2):
			new_circuit.cx(path[i], path[i + 1])
			new_circuit.cx(path[i + 1], path[i])
			new_circuit.cx(path[i], path[i + 1])

			current_q_1 = qubit_map[path[i]]
			current_q_2 = qubit_map[path[i + 1]]
			qubit_map[path[i]] = current_q_2
			qubit_map[path[i + 1]] = current_q_1

		inv_q_map = {v: k for k, v in qubit_map.items()}
		target_qubits = [inv_q_map[qubit] for qubit in qubits]
		new_circuit.append(instruction.operation, target_qubits)

	return new_circuit, {v: k for k, v in inv_q_map.items()}

	
# from analyser.extra import random_CX_circuit
# from analyser.architectures import square_grid, minimum_viable
# import time
# qubits = 200
# arc = minimum_viable(square_grid, qubits)
# circ = random_CX_circuit(qubits, qubits * 10, "qiskit")
# print("start")
# start = time.time()
# routed, q_map = dummy_router(circ, arc)
# end = time.time()
# print("runtime:", end - start)
# print(q_map)
