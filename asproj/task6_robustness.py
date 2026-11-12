import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import config
from .plotting import save

FRACTIONS = [0, 0.01, 0.02, 0.05, 0.10]
TRIALS = 10


def surviving_fraction(g, removed):
    remaining = [a for a in g.nodes if a not in removed]
    alive = sum(1 for a in remaining if any(n not in removed for n in g.neighbors[a]))
    return alive / len(remaining)


def random_removal(g, f, seed):
    nodes = sorted(g.nodes)
    rng = np.random.default_rng(seed)
    return set(rng.choice(nodes, size=int(f * len(nodes)), replace=False).tolist())


def targeted_removal(g, f):
    ranked = sorted(g.nodes, key=g.degree, reverse=True)
    return set(ranked[: int(f * len(ranked))])


def plot_robustness(random_results, targeted_results):
    fig, ax = plt.subplots(figsize=(7, 5))
    x = [100 * f for f in FRACTIONS]
    ax.plot(x, random_results["mean"], marker="o", label=f"Random (mean of {TRIALS} trials, min–max band)")
    ax.fill_between(x, random_results["min"], random_results["max"], alpha=0.3)
    ax.plot(x, targeted_results, marker="s", label="Targeted (highest degree first)")
    ax.set_xlabel("ASes removed, f (%)")
    ax.set_ylabel("R(f) = surviving ASes with degree > 0 / remaining ASes")
    ax.set_title("Graph 7: Robustness under AS removal")
    ax.legend()
    ax.grid(alpha=0.3)
    save(fig, "graph7_robustness")


def run(g):
    print("== Task 6: Robustness ==")
    trials = [[surviving_fraction(g, random_removal(g, f, config.SEED + t)) for t in range(TRIALS)] for f in FRACTIONS]
    random_results = pd.DataFrame({
        "f": FRACTIONS,
        "mean": [np.mean(r) for r in trials],
        "std": [np.std(r) for r in trials],
        "min": [min(r) for r in trials],
        "max": [max(r) for r in trials],
    })
    random_results["targeted"] = [surviving_fraction(g, targeted_removal(g, f)) for f in FRACTIONS]
    print(random_results.round(4).to_string(index=False), "\n")
    random_results.to_csv(config.OUT_DIR / "task6_robustness.csv", index=False)
    plot_robustness(random_results, random_results["targeted"])
