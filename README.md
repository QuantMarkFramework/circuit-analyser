# circuit-analyser
A python library for analysing quantum circuits and architectures.

# This library is work in progress.

## Example of comparing architectures.
```python
from analyser.extra import random_CX_H_T_circuit
from analyser import PytketAnalyzer
from analyser.architectures import big_hexagons, square_grid, fully_connected
from analyser.architectures import qubits_to_connections, stack
import math

qubit_counts = range(20, 60, 20)
n = 2
placement = "linear"


def qubes(qubits=0, n=0):
	if not n:
		n = math.ceil(qubits ** (1 / 3) - 1)
	arc = square_grid(n=n + 1)
	return stack(arc, n + 1)


def big_qubes(qubits):
	root = (8 * qubits + 4 * math.sqrt(qubits * (4 * qubits + 1)) + 1) ** (1 / 3)
	n = math.ceil((root + 1 / root - 3) / 4)
	arc = qubes(n=n)
	return qubits_to_connections(arc)


arcfs = [fully_connected, big_hexagons, square_grid, qubes, big_qubes]

headers = ["qubits"]
for arc in ["fully_connected", "big_hexagons", "square_grid", "qubes", "big_qubes"]:
	headers.append(arc + "_depth")
	headers.append(arc + "_count")
print(",".join(headers))

analyzer = PytketAnalyzer(placement)
for qubits in qubit_counts:
	cnots = qubits * 10
	arcs = [f(qubits) for f in arcfs]
	for _ in range(n):
		circ = random_CX_H_T_circuit(qubits=qubits, cnots=cnots)
		res = analyzer.analyse(
			circ,
			architecture=arcs,
		)
		print(qubits, end="")
		for r in res:
			print(",", r.gate_depth, ",", r.gate_count, sep="", end="")
		print()
```
