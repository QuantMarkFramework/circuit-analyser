import typing
import tequila as tq
from pytket import Circuit
from pytket.circuit import fresh_symbol
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

SUPPORTED_GATES = [*GATE_MAP.keys()]  # "Exp-Pauli", # TODO

COMPILER_ARGUMENTS = {
	"multitarget": True,
	"multicontrol": True,
	"trotterized": True,
	"generalized_rotation": True,
	"exponential_pauli": True,
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
				original_parameter = gate.parameter
				if isinstance(original_parameter, FixedVariable):
					parameter = float(original_parameter) / np.pi
				elif variables:
					parameter = original_parameter(variables) / np.pi
				elif isinstance(original_parameter, Variable):
					parameter = variable_map.get(original_parameter.name, None)
					if not parameter:
						parameter = fresh_symbol(str(original_parameter.name)) / np.pi
						variable_map[original_parameter.name] = parameter
				elif isinstance(original_parameter, Objective):
					raise TequilaToTketTranslationError(
						"Objectives as parameters are not supported."  # Maybe doable
					)
				else:
					raise TequilaToTketTranslationError(
						f'Parameter of type {type(original_parameter)} is not supported'
					)
				gate_function[n_control](c)(parameter, *gate.control, *gate.target)
			else:
				gate_function[n_control](c)(*gate.control, *gate.target)
		elif gate.name == "Exp-Pauli":
			raise TequilaToTketTranslationError(
				"Exp-Pauli gatese not YET supported"  # TODO
			)
		else:
			raise TequilaToTketTranslationError(
				f'Gate {gate.name} not supported.'
			)

	return c
