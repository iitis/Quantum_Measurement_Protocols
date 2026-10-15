"""Regenerate figures/fig_qubits_vs_N.pdf: quantum memory Q vs. number of queries N
for the qubit SIC POVM (d=2, n=4), exact constructions only."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import calculations as c

d, n, N_max = 2, 4, 500
Ns = list(range(1, N_max + 1))
lg = lambda A: [math.ceil(math.log2(A[N])) for N in Ns]
A_cq = c.max_type_product_all(N_max, n, lambda m: c.K_D_littlewood(m, d))
A_r1 = c.max_type_product_all(N_max, n, lambda m: c.comb(m + d - 1, d - 1))

curves = [  # (label, values, colour, linestyle)
    (r"Direct, uncompressed",            [c.qubits_direct(N, d) for N in Ns], "k",  "-"),
    (r"Naimark, canonical ($D=8$)",                               [c.qubits_naimark(N, d * n) for N in Ns], "C3", "-"),
    (r"Naimark, minimal ($D=4$)",       [c.qubits_naimark(N, n) for N in Ns], "C2", "-"),
    (r"Direct, compressed",                      lg(A_cq), "C0", "-"),
    (r"Direct, rank one, type classical", lg(A_r1), "C0", "--"),
    (r"Direct, rank one, $C=0$", [math.ceil(math.log2(c.comb(N + n * d - 1, N))) for N in Ns], "C0", ":"),
]

fig, (ax, bx) = plt.subplots(1, 2, figsize=(10, 4.0))
for lab, ys, col, ls in curves:
    ax.plot(Ns, ys, color=col, ls=ls, lw=1.8, label=lab)
for lab, ys, col, ls in curves[1:]:
    bx.plot(Ns, ys, color=col, ls=ls, lw=1.8)
for a, title in ((ax, "(a) all registers"), (bx, "(b) polynomial registers")):
    a.set_xlabel(r"number of oracle queries $N$"); a.set_xlim(1, N_max); a.grid(alpha=0.25); a.set_title(title, fontsize=10)
ax.set_ylabel(r"quantum memory $Q$ [qubits]"); ax.set_ylim(0, N_max + 10)
bx.set_ylim(0, 1.05 * max(curves[1][1]))
ax.legend(fontsize=8.5, loc="upper left", frameon=False)

out = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures", "fig_qubits_vs_N.pdf"))
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.tight_layout(); fig.savefig(out)
print("wrote", out)
print("Q at N=%d:" % N_max, {lab.split(" (")[0].split(":")[0]: ys[-1] for lab, ys, _, _ in curves})
