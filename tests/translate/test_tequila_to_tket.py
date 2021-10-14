import unittest
import numpy as np
from sympy import Symbol
import tequila as tq
from analyser.translate import tequila_to_tket
from pytket import Circuit
from pytket.circuit import Pauli, PauliExpBox

# Missing tests
# test pregiven variables, also behaviour with object
# maybe some kind of test for compile


def s(name):
	return Symbol(name)


class TestTequilaToTket(unittest.TestCase):
	def test_basic_sigle_qubit_gates(self):
		circuit: tq.QCircuit = tq.gates.X(target=0) + tq.gates.Y(target=0)
		circuit += tq.gates.Z(target=0) + tq.gates.H(target=0)
		result: Circuit = tequila_to_tket(circuit=circuit)

		c: Circuit = Circuit(1).X(0).Y(0).Z(0).H(0)
		self.assertEqual(c, result)

	def test_basic_controlled_gates(self):
		circuit: tq.QCircuit = tq.gates.X(target=0, control=[1, 2])
		circuit += tq.gates.X(target=0, control=1) + tq.gates.Y(target=0, control=1)
		circuit += tq.gates.Z(target=0, control=1) + tq.gates.H(target=0, control=1)
		result: Circuit = tequila_to_tket(circuit=circuit)

		c: Circuit = Circuit(3).CCX(1, 2, 0).CX(1, 0).CY(1, 0).CZ(1, 0).CH(1, 0)

		self.assertEqual(c, result)

	def test_parametrized_gates(self):
		circuit: tq.QCircuit = tq.gates.Rx(angle=np.pi, target=0)
		circuit += tq.gates.Ry(angle=np.pi, target=0)
		circuit += tq.gates.Rz(angle=np.pi, target=0)
		circuit += tq.gates.Rx(angle=np.pi, target=1, control=0)
		circuit += tq.gates.Ry(angle=np.pi, target=1, control=0)
		circuit += tq.gates.Rz(angle=np.pi, target=1, control=0)
		result: Circuit = tequila_to_tket(circuit=circuit)

		c: Circuit = Circuit(2).Rx(1, 0).Ry(1, 0).Rz(1, 0)
		c.CRx(1, 0, 1).CRy(1, 0, 1).CRz(1, 0, 1)
		self.assertEqual(c, result)

	def test_parametrized_gates_with_symbols(self):
		circuit: tq.QCircuit = tq.gates.Rx(angle="x1", target=0)
		circuit += tq.gates.Ry(angle="x2", target=0)
		circuit += tq.gates.Rz(angle="x3", target=0)
		circuit += tq.gates.Rx(angle="x4", target=1, control=0)
		circuit += tq.gates.Ry(angle="x5", target=1, control=0)
		circuit += tq.gates.Rz(angle="x6", target=1, control=0)
		result: Circuit = tequila_to_tket(circuit=circuit)

		c: Circuit = Circuit(2).Rx(s("x1") / np.pi, 0).Ry(s("x2") / np.pi, 0)
		c.Rz(s("x3") / np.pi, 0).CRx(s("x4") / np.pi, 0, 1)
		c.CRy(s("x5") / np.pi, 0, 1).CRz(s("x6") / np.pi, 0, 1)
		self.assertEqual(c, result)

	def test_swap_gate(self):
		circuit: tq.QCircuit = tq.gates.SWAP(first=0, second=1)
		circuit += tq.gates.SWAP(first=1, second=2, control=0)
		result: Circuit = tequila_to_tket(circuit=circuit)

		c: Circuit = Circuit(3).SWAP(0, 1).CSWAP(0, 1, 2)
		self.assertEqual(c, result)

	def test_exp_pauli_gate(self):
		tq_paulistring: tq.PauliString = tq.PauliString({0: 'X', 2: 'Y'}, coeff=0.5)
		circuit: tq.QCircuit = tq.gates.ExpPauli(tq_paulistring, 0.5 * np.pi)
		result: Circuit = tequila_to_tket(circuit=circuit)

		pbox: PauliExpBox = PauliExpBox([Pauli.X, Pauli.Y], 0.25)
		c: Circuit = Circuit(3).add_pauliexpbox(pbox, [0, 2])

		# pytket does not seem to have PauliExpBox comaring implemeted
		c_com = c.get_commands()[0]
		res_com = result.get_commands()[0]

		self.assertEqual(c_com.op.get_paulis(), c_com.op.get_paulis())
		self.assertEqual(res_com.op.get_phase(), res_com.op.get_phase())
		self.assertEqual(c_com.qubits, res_com.qubits)
