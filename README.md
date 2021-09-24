# circuit-analyser
A python library for analysing quantum circuits.

# This library is not yet ready to be used.

## Example
```python
from analyser import analyse
import tequila as tq

mol = tq.Molecule(
	geometry="H 0.0 0.0 0\nO 0 0 1\nH 0 0 2",
	basis_set="cc-pVTZ",
	transformation="JORDANWIGNER"
)

U = mol.make_upccgsd_ansatz()

print("upccgsd")
print(analyse(U))

U2 = mol.make_uccsd_ansatz(trotter_steps=1)

print("uccsd")
print(analyse(U2, give_values=True))
```
