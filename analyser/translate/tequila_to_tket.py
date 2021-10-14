import typing
import tequila as tq
from pytket import Circuit
from pytket.circuit import fresh_symbol, Pauli, PauliExpBox
from tequila.circuit.compiler import Compiler
from tequila.objective.objective import FixedVariable, Objective, Variable
import numpy as np

GATE_MAP = {
	"X": (lambda c: c.X, lambda c: c.CX, lambda c: c.CCX),
	"Y": (lambda c: c.Y, lambda c: c.CY),
	"Z": (lambda c: c.Z, lambda c: c.CZ),
	"H": (lambda c: c.H, lambda c: c.CH),
	"SWAP": (lambda c: c.SWAP, lambda c: c.CSWAP),
	"Rx": (lambda c: c.Rx, lambda c: c.CRx),
	"Ry": (lambda c: c.Ry, lambda c: c.CRy),
	"Rz": (lambda c: c.Rz, lambda c: c.CRz),
}

PAULI_MAP = {
	"I": Pauli.I,
	"X": Pauli.X,
	"Y": Pauli.Y,
	"Z": Pauli.Z,
}

SUPPORTED_GATES = ["Exp-Pauli", *GATE_MAP.keys()]

COMPILER_ARGUMENTS = {
	"multitarget": True,
	"multicontrol": True,
	"trotterized": True,
	"generalized_rotation": True,
	"exponential_pauli": False,
	"controlled_exponential_pauli": True,
	"hadamard_power": True,
	"controlled_power": True,
	"power": True,
	"toffoli": False,
	"controlled_phase": False,
	"phase": True,
	"phase_to_z": True,
	"controlled_rotation": False,
	"swap": False,
	"cc_max": True,
	"ry_gate": False,
	"y_gate": False,
	"ch_gate": False
}


class TequilaToTketTranslationError(Exception):
	pass


# warning: transfers all parameters to strings
def translate_parameter(
	parameter,
	variable_map,
	variables
):
	if isinstance(parameter, FixedVariable):
		return float(parameter) / np.pi
	elif variables:
		return parameter(variables) / np.pi
	elif isinstance(parameter, Variable):
		new_parameter = variable_map.get(parameter.name, None)
		if not new_parameter:
			# print warning when dublicate string?
			new_parameter = fresh_symbol(str(parameter.name)) / np.pi
			variable_map[parameter.name] = new_parameter
		return new_parameter
	elif isinstance(parameter, Objective):
		raise TequilaToTketTranslationError(
			"Objectives as parameters are not supported."  # Maybe doable
		)
	else:
		raise TequilaToTketTranslationError(
			f'Parameter of type {type(parameter)} is not supported'
		)


def tequila_to_tket(
	circuit: tq.QCircuit,
	variables: typing.Dict[typing.Hashable, float] = None,
	compile: bool = False
) -> Circuit:
	if compile:
		circuit = Compiler(**COMPILER_ARGUMENTS)(circuit)
	c = Circuit(circuit.n_qubits)
	variable_map = {}

	for gate in circuit.gates:
		gate_function = GATE_MAP.get(gate.name, None)
		if gate_function:
			n_control = len(gate.control)
			valid_swap: bool = len(gate.target) == 2 and gate.name == "SWAP"
			if not len(gate.target) == 1 and not valid_swap:
				raise TequilaToTketTranslationError(
					"Translating of multi target gates (except SWAP)is not supported."
				)
			if n_control > len(gate_function) - 1:
				raise TequilaToTketTranslationError(
					f'Translating {gate.name} with {n_control} controls is not supported.'
				)
			if gate.is_parametrized():
				parameter = translate_parameter(gate.parameter, variable_map, variables)
				gate_function[n_control](c)(parameter, *gate.control, *gate.target)
			else:
				gate_function[n_control](c)(*gate.control, *gate.target)
		elif gate.name == "Exp-Pauli":
			if not len(gate.control) == 0:
				raise TequilaToTketTranslationError(
					"Can not translate controlled Exp-Pauli gates."
				)
			paulis = []
			qubits = []
			for qubit, pauli in gate.paulistring.items():
				paulis.append(PAULI_MAP[pauli.upper()])
				qubits.append(qubit)
			coeff = gate.paulistring.coeff
			if gate.is_parametrized():
				parameter = translate_parameter(gate.parameter, variable_map, variables)
				coeff *= parameter
			pbox = PauliExpBox(paulis, coeff)
			c.add_pauliexpbox(pbox, qubits)
		else:
			raise TequilaToTketTranslationError(
				f'Gate {gate.name} not supported.'
			)

	return c
