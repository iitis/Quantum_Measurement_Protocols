# Quantum_Measurement_Protocols

Code accompanying the manuscript *Quantum and Classical Memory for Storage and Retrieval of Quantum Measurements*
by F. Turoboś, L. Marcinkowska and Z. Puchała.

The code computes every register size and success probability quoted in the manuscript: Tables 1, 2 and 4, Figure 1, and the numerical values in the text.

## Reproduce the tables and the figure

```bash
pip install -r requirements.txt
python numerical_supplement/make_tables.py       # prints the rows of Tables 2 and 4 as LaTeX
python numerical_supplement/make_fig_qubits.py   # writes figures/fig_qubits_vs_N.pdf (Figure 1)
```

Tested in clean environments with Python 3.9 (numpy 1.24, pandas 2.0, matplotlib 3.7) and Python 3.12 (numpy 2.5, pandas 3.0, matplotlib 3.11).

Table 1 is the row $d=2$, $n=4$, $N=50$ of Table 2; Table 3 is symbolic.
SciPy is not required. All combinatorics use exact integer arithmetic, and the maximum over outcome types is computed exactly by dynamic programming, without assuming log-concavity.

## What `calculations.py` computes

| function | quantity | manuscript |
|---|---|---|
| `dim_direct`, `qubits_direct`, `classical_direct` | uncompressed direct program | Proposition 14 |
| `K_D`, `K_D_littlewood` | retained dimension $K_D(m)$, via the Weyl sum and via Littlewood's identity | Lemma 11, Eq. (14) |
| `max_type_product`, `max_type_product_all` | exact maximum over outcome types | — |
| `qubits_direct_cq`, `classical_direct_cq` | compressed direct program | Proposition 16 |
| `qubits_direct_rank1`, `qubits_direct_rank1_quantum` | rank-one refinement, type kept classical / type in the quantum register | Proposition 18 |
| `dim_naimark_D`, `qubits_naimark` | Naimark register for dilation dimension $D$ | Theorem 36 |
| `dim_branch`, `qubits_branch_ppbt`, `classical_branch_table` | branch program with a finite classical table | Theorem 41, Proposition 42 |
| `qubits_measured_branch`, `classical_measured_branch` | measured-branch program, type kept classical | Proposition 43 |
| `qubits_measured_branch_quantum` | measured-branch program, type in the quantum register | Corollary 44 |
| `success_*` | heralded success probabilities | — |

The remaining functions in `calculations.py` (`generate_memory_sweep`, `comparison_summary`, `log_memory_*`, …) come from earlier drafts. They compare uncompressed program dimensions and are not used for any result in the manuscript.

## License

MIT (see `LICENSE`).
