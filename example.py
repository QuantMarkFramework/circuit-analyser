from analyser import analyse
import tequila as tq

mol = tq.Molecule(
	geometry="Li 0.0 0.0 0\nH 0 0 1",
	basis_set="cc-pVDZ",
	transformation="JORDANWIGNER"
)

U = mol.make_upccgsd_ansatz()

print("upccgsd")
print(analyse(U))

for initial_amplitudes in ["mp2", "cc2", "ccsd"]:
	U2 = mol.make_uccsd_ansatz(initial_amplitudes=initial_amplitudes, trotter_steps=1)
	print(U2)
	print("uccsd with initial amplitudes:", initial_amplitudes)
	print(analyse(U2, give_values=True))
