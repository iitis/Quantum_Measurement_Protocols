"""Rows of the numerical tables of the manuscript, as LaTeX: Table 2 (tab:numerical) and Table 4 (tab:branch).
Table 3 (tab:memoryQC) is symbolic; Table 1 (tab:benchmark) is the d=2, n=4, N=50 row of Table 2."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calculations as c

SYSTEMS = [(2, 2), (2, 4), (2, 6), (2, 8), (3, 9)]
lam = lambda N, D: N / (N - 1 + D * D)
tex = lambda row: " & ".join(f"${x}$" for x in row) + r" \\"


def table1_rows(Ns=(10, 50, 100)):
    """d n N | Direct Q C | compressed Q C | rank-one Q Q^q | Nai_min Q | Branch Q C | P_dir P_nmin P_br"""
    rows = []
    for d, n in SYSTEMS:
        for N in Ns:
            rows.append(((d, n, N), tex([d, n, N,
                c.qubits_direct(N, d), c.classical_direct(N, n),
                c.qubits_direct_cq(N, d, n), c.classical_direct_cq(N, n),
                c.qubits_direct_rank1(N, d, n), c.qubits_direct_rank1_quantum(N, d, n),
                c.qubits_naimark(N, n), c.qubits_branch_ppbt(N, d), c.classical_branch_table(n, d),
                f"{lam(N, d):.3f}", f"{lam(N, n):.3f}", f"{lam(N, 2 * d) / 8:.3f}"])))
    return rows


def table3_rows(Ns=(50, 200)):
    """d n N | full-unitary Q C P | measured, type classical Q C P | measured, type quantum Q C"""
    rows = []
    for d, n in SYSTEMS:
        for N in Ns:
            rows.append(((d, n, N), tex([d, n, N,
                c.qubits_branch_ppbt(N, d), c.classical_branch_table(n, d), f"{lam(N, 2 * d) / 8:.4f}",
                c.qubits_measured_branch(N, d), c.classical_measured_branch(N, d, n), f"{lam(N, d) / 8:.4f}",
                c.qubits_measured_branch_quantum(N, d), c.classical_branch_table(n, d)])))
    return rows


if __name__ == "__main__":
    print("% tab:numerical:", table1_rows.__doc__)
    for _, r in table1_rows():
        print(r)
    print("% tab:branch:", table3_rows.__doc__)
    for _, r in table3_rows():
        print(r)
