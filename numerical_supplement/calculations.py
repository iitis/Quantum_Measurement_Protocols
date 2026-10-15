from math import comb as _math_comb


def comb(n, k, exact=True):
    """Binomial coefficient (exact integer); drop-in for scipy.special.comb(..., exact=True)."""
    return _math_comb(n, k)
import numpy as np
import pandas as pd
import math

def dim_naimark(N, d, n):
    "Memory dimension: Naimark route"
    exponent = (d * n) ** 2
    return comb(N + exponent - 1, N, exact=True)

def dim_naimark_min(N, d, n):
    "Minimal Naimark dilation dimension for rank-one POVM"
    # For rank-one POVM: D_min = n (not dn!)
    D_min = n
    return comb(N + D_min ** 2 - 1, N, exact=True)

def dim_naimark_D(N, D):
    "Memory dimension for a Naimark dilation of dimension D."
    return comb(N + D**2 - 1, N, exact=True)

def dim_branch(N, d):
    "Memory dimension: Branch-coherent route"
    exponent = (2 * d) ** 2
    return comb(N + exponent - 1, N, exact=True)

def dim_direct(N, d, n):
    "Memory dimension: Direct route (exponential in N, depends on both d and n)"
    N = int(N)
    return (d * n) ** N

def qubits_direct(N, d):
    "Coherent quantum memory for the direct route."
    return math.ceil(N * math.log2(d))

def classical_direct(N, n):
    "Classical outcome record for the direct route."
    return math.ceil(N * math.log2(n))

def qubits_branch_dpbt(N, d):
    "Coherent quantum memory for the deterministic-PBT branch route."
    return math.ceil(N * math.log2(2 * d))

def classical_branch_dpbt(N, n):
    "Classical outcome record for the deterministic-PBT branch route."
    return math.ceil(N * math.log2(n + 1))

def qubits_naimark(N, D):
    "Coherent quantum memory for a Naimark PSAR register of dimension D."
    return math.ceil(math.log2(dim_naimark_D(N, D)))

def qubits_branch_ppbt(N, d):
    "Coherent quantum memory for the branch pPBT route."
    return math.ceil(math.log2(dim_branch(N, d)))
    
def success_naimark(N, d, n, D_nai=None):
    """Success probability: Naimark route.

    Args:
        D_nai: Actual dilation dimension. If None, uses D_nai = d*n
               corresponding to the non-minimal construction.
    """
    if D_nai is None:
        D_nai = d * n

    return N / (N - 1 + D_nai ** 2)

def success_branch(N, d):
    "Success probability: Branch-coherent route (includes q=1/8 factor)"
    return (1/8) * N / (N - 1 + 4 * d ** 2)

def success_direct(N, d, n):
    "Success probability: Direct route (depends only on d, not n)"
    return N / (N - 1 + d ** 2)

def _cmp(a, b):
    return "<" if a < b else ("=" if a == b else ">")

def validate_row(N, d, n):
    """
    Check whether theoretical properties are satisfied.
    """

    dimN = dim_naimark(N, d, n)
    dimN_min = dim_naimark_min(N, d, n)
    dimB = dim_branch(N, d)
    dimD = dim_direct(N, d, n)

    sucN = success_naimark(N, d, n)
    sucN_min = success_naimark(N, d, n, D_nai=n)
    sucB = success_branch(N, d)
    sucD = success_direct(N, d, n)

    return {
        "memory_check_nonminimal":
            "N/A" if n < 3 else (dimN > dimB),

        "memory_check_minimal": 
            _cmp(dimN_min, dimB) == _cmp(n, 2 * d),

        "success_range":
            (0 <= sucN <= 1)
            and (0 <= sucN_min <= 1)
            and (0 <= sucB <= 1)
            and (0 <= sucD <= 1),

        "dimension_positive":
            (dimN > 0)
            and (dimN_min > 0)
            and (dimB > 0)
            and (dimD > 0)
    }

    import pandas as pd


def generate_memory_sweep(systems, N_values):
    rows = []

    for _, system in systems.iterrows():
        d = int(system["d"])
        n = int(system["n"])
        description = system["description"]

        for N in N_values:
            validation = validate_row(N, d, n)

            rows.append({
                "d": d,
                "n": n,
                "description": description,
                "N": N,
                "dim_Direct": dim_direct(N, d, n),
                "dim_Naimark_minimal": dim_naimark_min(N, d, n),
                "dim_Naimark": dim_naimark(N, d, n),
                "dim_Branch": dim_branch(N, d),
                "success_Direct": success_direct(N, d, n),
                "success_Naimark_minimal": success_naimark(N, d, n, D_nai=n),
                "success_Naimark": success_naimark(N, d, n),
                "success_Branch": success_branch(N, d),
                
                **validation,
            })

    table = pd.DataFrame(rows)

    memory_columns = [
        "dim_Direct",
        "dim_Naimark_minimal",
        "dim_Naimark",
        "dim_Branch",
    ]

    for col in memory_columns:
        table[col] = table[col].apply(lambda x: f"{float(x):.3e}")

    success_columns = [
        "success_Direct",
        "success_Naimark_minimal",
        "success_Naimark",
        "success_Branch",
    ]

    for col in success_columns:
        table[col] = table[col].apply(lambda x: f"{x:.4f}")

    return table
    
def comparison_summary(d, n):
    """
    Compare minimal and non-minimal Naimark constructions
    with the Branch-coherent construction.
    """

    delta_memory_exponent_min = n**2 - 4*d**2
    delta_memory_exponent_nonmin = d**2 * (n**2 - 4)

    threshold_min = max(
    1,
    math.ceil(1 + (n**2 - 32*d**2) / 7)
    )

    threshold_nonmin = max(
    1,
    math.ceil(1 + d**2 * (n**2 - 32) / 7)
    )

    return {
        "d": d,
        "n": n,
        "delta_memory_exponent_min": delta_memory_exponent_min,
        "delta_memory_exponent_nonmin": delta_memory_exponent_nonmin,
        "N_threshold_Naimark_min_success": threshold_min,
        "N_threshold_Naimark_nonmin_success": threshold_nonmin,
    }   

def log_memory_naimark(N, d, n):
    return math.log10(dim_naimark(N, d, n))

def log_memory_branch(N, d):
    return math.log10(dim_branch(N, d))

def log_memory_direct(N, d, n):
    return N * math.log10(d * n)

def log_memory_naimark_min(N, d, n):
    return math.log10(dim_naimark_min(N, d, n))

def n_port_for_budget(b, d):
    "Maximum number of queries for measured-port storage within b qubits."
    return int(b // math.log2(d))

def n_coh_for_budget(b, d):
    "Maximum number of queries for coherent branch storage within b qubits."
    N = 1
    while dim_branch(N + 1, d) <= 2 ** b:
        N += 1
    return N

def p_port(N, d, q=1/8):
    "Heralded success probability for the port-based route."
    return q * N / (N - 1 + d ** 2)

def p_coh(N, d, q=1/8):
    "Heralded success probability for the coherent branch route."
    return q * N / (N - 1 + 4 * d ** 2)


# ---------------------------------------------------------------------------
# Compressed direct program (Proposition prop:direct-cq) and rank-one refinement
# ---------------------------------------------------------------------------

def _partitions(m, max_parts, max_part=None):
    """Partitions of m into at most max_parts parts, parts non-increasing."""
    if max_part is None:
        max_part = m
    if m == 0:
        yield ()
        return
    if max_parts == 0:
        return
    for first in range(min(m, max_part), 0, -1):
        for rest in _partitions(m - first, max_parts - 1, first):
            yield (first,) + rest


def _weyl_dim(lam, D):
    """Dimension of the U(D) irrep with Young diagram lam (Weyl formula)."""
    l = list(lam) + [0] * (D - len(lam))
    num = den = 1
    for i in range(D):
        for j in range(i + 1, D):
            num *= (l[i] - l[j] + j - i)
            den *= (j - i)
    return num // den


_K_cache = {}


def K_D(m, D):
    """K_D(m) = sum over lam |- m, len(lam) <= D of dim U_lam  (eq. eq:KD).
    K_D(0) = 1. For D = 2 this equals (floor(m/2)+1)(ceil(m/2)+1)."""
    if m == 0:
        return 1
    if (m, D) not in _K_cache:
        _K_cache[(m, D)] = sum(_weyl_dim(l, D) for l in _partitions(m, min(D, m)))
    return _K_cache[(m, D)]


# ---------------------------------------------------------------------------
# Exact evaluation of K_D via Littlewood's identity and exact type maximization
# (log-concavity of K_D is NOT assumed)
# ---------------------------------------------------------------------------

def K_D_littlewood(m, D):
    """K_D(m) = [z^m] (1-z)^{-D} (1-z^2)^{-D(D-1)/2}  (Littlewood/Schur identity).
    For D >= 2:  sum_k binom(m-2k+D-1, D-1) * binom(k+b-1, b-1), b = D(D-1)/2."""
    if m == 0:
        return 1
    b = D * (D - 1) // 2
    if b == 0:
        return comb(m + D - 1, D - 1, exact=True)
    return sum(comb(m - 2 * k + D - 1, D - 1, exact=True) * comb(k + b - 1, b - 1, exact=True)
               for k in range(m // 2 + 1))


def max_type_product(N, n, f):
    """Exact max over types t in T_{n,N} (n nonnegative integers summing to N)
    of prod_j f(t_j), by dynamic programming. No log-concavity assumed."""
    A = [1] + [0] * N
    for _ in range(n):
        A = [max(A[s - m] * f(m) for m in range(s + 1)) for s in range(N + 1)]
    return A[N]


def qubits_direct_cq(N, d, n):
    """Q of the compressed direct program (exact maximization over types)."""
    return math.ceil(math.log2(max_type_product(N, n, lambda m: K_D_littlewood(m, d))))


def classical_direct_cq(N, n):
    """C of the compressed direct program: ceil(log2 binom(N+n-1, n-1)), the number of outcome types."""
    return math.ceil(math.log2(comb(N + n - 1, n - 1, exact=True)))


def qubits_direct_rank1(N, d, n):
    """Q for rank-one POVMs (exact maximization over types)."""
    return math.ceil(math.log2(max_type_product(N, n, lambda m: comb(m + d - 1, d - 1, exact=True))))


def qubits_measured_branch(N, d):
    """Q of the measured-branch program: rank-one encoder on the 2d-outcome raw readout."""
    return qubits_direct_rank1(N, d, 2 * d)


def classical_measured_branch(N, d, n):
    """C of the measured-branch program: raw-outcome type + relabelling table."""
    return math.ceil(math.log2(comb(N + 2 * d - 1, 2 * d - 1, exact=True))) + 2 * d * math.ceil(math.log2(n + 1))


def max_type_product_all(N_max, n, f):
    """A[s] = max over types t in T_{n,s} of prod_j f(t_j), for every s = 0..N_max,
    from a single dynamic-programming pass (used to draw curves against N)."""
    fv = [f(m) for m in range(N_max + 1)]
    A = [1] + [0] * N_max
    for _ in range(n):
        A = [max(A[s - m] * fv[m] for m in range(s + 1)) for s in range(N_max + 1)]
    return A


def classical_branch_table(n, d):
    """C of the branch programs with an N-independent record: the sampled table of 2d labels in {1,...,n, empty}."""
    return 2 * d * math.ceil(math.log2(n + 1))


def qubits_direct_rank1_quantum(N, d, n):
    """Q of the rank-one direct program with the type stored in the quantum register (C = 0):
    ceil(log2 binom(N+nd-1, N)) = ceil(log2 sum_t prod_j binom(t_j+d-1, d-1))   (eq. direct-rank1-quantum)."""
    return math.ceil(math.log2(comb(N + n * d - 1, N)))


def qubits_measured_branch_quantum(N, d):
    """Q of the measured-branch program with the raw-outcome type in the quantum register (Cor. measured-branch-quantum)."""
    return qubits_direct_rank1_quantum(N, d, 2 * d)
