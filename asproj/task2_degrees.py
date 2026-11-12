import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import config
from .plotting import save

BINS = [(0, 0), (1, 1), (2, 5), (6, 100), (101, 500), (501, 1000), (1001, None)]
COLUMNS = {"degree": "Global degree", "customers": "Customer degree", "peers": "Peer degree", "providers": "Provider degree"}


def degree_table(g):
    """DataFrame: asn, degree, customers, peers, providers"""
    return pd.DataFrame(
        [(a, g.degree(a), g.customer_degree(a), g.peer_degree(a), g.provider_degree(a)) for a in list(g.nodes)],
        columns=["asn", "degree", "customers", "peers", "providers"],
    )


def validate_identity(deg_df):
    bad = deg_df[deg_df["degree"] != deg_df["customers"] + deg_df["peers"] + deg_df["providers"]]
    print(f"Identity d = dc + dp + dr violated for {len(bad)} of {len(deg_df):,} ASes")
    return bad


def bin_counts(values):
    labels, counts = [], []
    for lo, hi in BINS:
        labels.append(f">{lo - 1}" if hi is None else (str(lo) if lo == hi else f"{lo}-{hi}"))
        counts.append(int(((values >= lo) & (values <= (hi if hi is not None else np.inf))).sum()))
    return labels, counts


def plot_graph2_histograms(deg_df):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    for ax, (col, title) in zip(axes.flat, COLUMNS.items()):
        labels, counts = bin_counts(deg_df[col])
        ax.bar(labels, counts)
        ax.set_yscale("log")
        ax.set_title(title)
        ax.set_xlabel("Degree bin")
        ax.set_ylabel("Number of ASes (log)")
        for i, c in enumerate(counts):
            ax.annotate(f"{c:,}", (i, max(c, 1)), ha="center", va="bottom", fontsize=8)
    fig.suptitle(f"Graph 2: Degree histograms (N = {len(deg_df):,} ASes in as-rel2 2024-11)")
    fig.tight_layout()
    save(fig, "graph2_degree_histograms")


def plot_graph3_ccdf(deg_df):
    d = np.sort(deg_df["degree"].values)
    ks = np.unique(d[d >= 1])
    ccdf = 1 - np.searchsorted(d, ks, side="left") / len(d)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(ks, ccdf, marker=".", linestyle="none")
    ax.set_xlabel("Global degree k")
    ax.set_ylabel("Pr(D ≥ k)")
    ax.set_title(f"Graph 3: CCDF of global AS degree (N = {len(d):,})")
    ax.grid(True, which="both", alpha=0.3)
    save(fig, "graph3_degree_ccdf")


def summary_stats(deg_df):
    d = deg_df["degree"]
    return {"mean": d.mean(), "median": d.median(), "p95": d.quantile(0.95), "max": d.max()}


def top_degree(deg_df, n=10):
    return deg_df.sort_values("degree", ascending=False).head(n).reset_index(drop=True)


def run(g):
    print("== Task 2: Degrees ==")
    deg = degree_table(g)
    validate_identity(deg)
    for col in COLUMNS:
        print(col, dict(zip(*bin_counts(deg[col]))))
    print("Global degree stats:", {k: round(float(v), 2) for k, v in summary_stats(deg).items()})
    top = top_degree(deg)
    print(top.to_string(), "\n")
    top.to_csv(config.OUT_DIR / "task2_top_degree.csv", index=False)
    plot_graph2_histograms(deg)
    plot_graph3_ccdf(deg)
