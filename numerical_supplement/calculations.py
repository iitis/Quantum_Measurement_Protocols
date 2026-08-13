from scipy.special import comb
import numpy as np
import pandas as pd
import math

def dim_naimark(N, d, n):
    """Memory dimension: Naimark route"""
    exponent = (d * n) ** 2
    return comb(N + exponent - 1, N, exact=True)

def dim_branch(N, d):
    """Memory dimension: Branch-coherent route"""
    exponent = (2 * d) ** 2
    return comb(N + exponent - 1, N, exact=True)

def dim_direct(N, d, n):
    """Memory dimension: Direct route (exponential in N, depends on both d and n)"""
    N = int(N)
    return (d * n) ** N

def dim_KK(N, d, e):
    """Program memory for the KK protocol."""
    exponent = (d * e) ** 2
    return comb(N + exponent - 1, N, exact=True)

def dim_Stinespring(N, d, e):
    """Program memory for the Stinespring protocol."""
    exponent = (d * e) ** 2
    return comb(N + exponent - 1, N, exact=True)

def success_naimark(N, d, n):
    """Success probability: Naimark route (same as Direct)"""
    return N / (N - 1 + (d * n) ** 2)

def success_branch(N, d):
    """Success probability: Branch-coherent route (includes q=1/8 factor)"""
    return (1/8) * N / (N - 1 + 4 * d ** 2)

def success_direct(N, d, n):
    """Success probability: Direct route (depends on effective dimension dn)"""
    return N / (N - 1 + (d * n) ** 2)

def validate_row(N, d, n):
    """
    Check whether theoretical properties are satisfied.
    """

    dimN = dim_naimark(N, d, n)
    dimB = dim_branch(N, d)
    dimD = dim_direct(N, d, n)

    sucN = success_naimark(N, d, n)
    sucB = success_branch(N, d)
    sucD = success_direct(N, d, n)

    return {
        "memory_check":
            #(dimN > dimB) if n >= 3 else np.nan,
            "N/A" if n < 3 else (dimN > dimB),

        "success_formula":
            (sucN > sucB) == (7*(N-1) + d**2*(32 - n**2) > 0),

        "success_range":
            (0 <= sucN <= 1)
            and (0 <= sucB <= 1)
            and (0 <= sucD <= 1),

        "dimension_positive":
            (dimN > 0)
            and (dimB > 0)
            and (dimD > 0)
    }

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
                "dim_Naimark": dim_naimark(N, d, n),
                "dim_Branch": dim_branch(N, d),

                "success_Direct": success_direct(N, d, n),
                "success_Naimark": success_naimark(N, d, n),
                "success_Branch": success_branch(N, d),

                **validation
            })

    table = pd.DataFrame(rows)

    # Format large memory dimensions using scientific notation
    memory_columns = [
        "dim_Direct",
        "dim_Naimark",
        "dim_Branch"
    ]

    for col in memory_columns:
        table[col] = table[col].apply(lambda x: f"{float(x):.3e}")
    # Format success probabilities
    success_columns = [
        "success_Direct",
        "success_Naimark",
        "success_Branch"
    ]

    for col in success_columns:
        table[col] = table[col].apply(lambda x: f"{x:.4f}")

    return table

    
def comparison_summary(d, n):
    """
    Compare Naimark and Branch constructions.
    """

    delta_memory_exponent = d**2 * (n**2 - 4)

    N_threshold = max(1,math.floor(1 + d**2*(n**2-32)/7) + 1)

    if delta_memory_exponent == 0:
        memory_comment = "Equal polynomial memory"
    else:
        memory_comment = "Naimark much worse for memory"

    success_comment = (
        f"Naimark success wins from N={N_threshold}"
    )

    return {
        "d": d,
        "n": n,
        "delta_memory_exponent": delta_memory_exponent,
        "N_threshold_Naimark_success": N_threshold,
        "comment": memory_comment + "; " + success_comment
    }

def log_memory_naimark(N, d, n):
    return math.log10(dim_naimark(N, d, n))

def log_memory_branch(N, d):
    return math.log10(dim_branch(N, d))

def log_memory_direct(N, d, n):
    return N * math.log10(d * n)
