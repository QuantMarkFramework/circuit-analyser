from analyser.architectures import fully_connected, linear, circle, square_grid
from analyser.architectures import octagons, hexagons, minimum_viable, qubits_to_connections
from analyser.extra import random_CX_circuit
from analyser.analyser import PytketAnalyser, QiskitAnalyser, DummyAnalyser
import random
import sys


# Parameters
lattice_qubit_count = 500
biggest_qubit_count = int(sys.argv[1])
runs = int(sys.argv[2])
random_seed = int(sys.argv[3])

dummy_method = ["dummy"]
qiskit_methods = ["None"]
pytket_methods = ["linear", "graph"]
qubit_counts = range(20, biggest_qubit_count + 20, 20)

arcfs = [
	fully_connected,
	lambda _: linear(lattice_qubit_count),
	circle,
	lambda _: minimum_viable(square_grid, lattice_qubit_count),
	lambda _: minimum_viable(octagons, lattice_qubit_count),
	lambda _: minimum_viable(hexagons, lattice_qubit_count),
	lambda _: minimum_viable(lambda n: qubits_to_connections(square_grid(n=n)), lattice_qubit_count),
	lambda _: minimum_viable(lambda n: qubits_to_connections(octagons(n=n)), lattice_qubit_count),
	lambda _: minimum_viable(lambda n: qubits_to_connections(hexagons(n=n)), lattice_qubit_count),
]

names = [
	"fully connected",
	"linear",
	"circle",
	"square",
	"square-octagon",
	"hexagon",
	"heavy-square",
	"heavy-square-octagon",
	"heavy-hexagon"
]

print("qubits", end="")
for method in dummy_method + qiskit_methods + pytket_methods:
	print(",", end="")
	for name in names[:-1]:
		print(f'{method}_{name}_depth', end=",")
		print(f'{method}_{name}_count', end=",")
		print(f'{method}_{name}_time', end=",")
	print(f'{method}_{names[-1]}_depth', end=",")
	print(f'{method}_{names[-1]}_count', end=",")
	print(f'{method}_{names[-1]}_time', end="")
print()

dummy_analyser = [DummyAnalyser(ignore_errors=True) for _ in dummy_method]
qiskit_analysers = [QiskitAnalyser(method, ignore_errors=True) for method in qiskit_methods]
pytket_analysers = [PytketAnalyser(method, ignore_errors=True) for method in pytket_methods]

for qubits in qubit_counts:
	cnots = qubits * 10
	arcs = [f(qubits) for f in arcfs]
	random.seed(random_seed)
	q_circ = [random_CX_circuit(qubits, cnots, "qiskit") for _ in range(runs)]
	random.seed(random_seed)
	p_circ = [random_CX_circuit(qubits, cnots, "pytket") for _ in range(runs)]
	for i in range(runs):
		dummy_results = [a.analyse(q_circ[i], arcs) for a in dummy_analyser]
		qiskit_results = [a.analyse(q_circ[i], arcs) for a in qiskit_analysers]
		pytket_results = [a.analyse(p_circ[i], arcs) for a in pytket_analysers]
		print(qubits, end="")
		for results in dummy_results + qiskit_results + pytket_results:
			for r in results:
				print(f',{r.gate_depth},{r.gate_count},{r.transpile_time}', end="")
		print()
