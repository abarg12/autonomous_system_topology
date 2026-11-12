import matplotlib.pyplot as plt
import pandas as pd

from . import config
from .plotting import save


def cone(g, asn):
    seen, stack = {asn}, [asn]
    while stack:
        for c in g.customers.get(stack.pop(), ()):
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return seen


def customer_cone_sizes(g) -> dict[int, int]:
    return {a: len(cone(g, a)) if g.customers.get(a) else 1 for a in list(g.nodes)}


def top_cones_table(g, cones, orgs, n=15):
    top = sorted(cones, key=cones.get, reverse=True)[:n]
    degree_rank = {a: i + 1 for i, a in enumerate(sorted(g.nodes, key=g.degree, reverse=True))}
    return pd.DataFrame({
        "rank": range(1, len(top) + 1),
        "asn": top,
        "organization": [orgs.get(a, "") for a in top],
        "degree": [g.degree(a) for a in top],
        "degree_rank": [degree_rank[a] for a in top],
        "customers": [g.customer_degree(a) for a in top],
        "cone_size": [cones[a] for a in top],
    })


def plot_graph6(cones, n=100):
    sizes = sorted(cones.values(), reverse=True)[:n]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(range(1, len(sizes) + 1), sizes, marker=".")
    ax.set_yscale("log")
    ax.set_xlabel("Cone rank")
    ax.set_ylabel("Customer-cone size (# ASes, log)")
    ax.set_title(f"Graph 6: Top {n} customer-cone sizes (2024 graph, N = {len(cones):,} ASes)")
    ax.grid(True, which="both", alpha=0.3)
    save(fig, "graph6_cones")


def run(g, orgs):
    print("== Task 5: Customer cones ==")
    cones = customer_cone_sizes(g)
    table = top_cones_table(g, cones, orgs)
    print(table.to_string(index=False))
    top100_cone = set(sorted(cones, key=cones.get, reverse=True)[:100])
    top100_deg = set(sorted(g.nodes, key=g.degree, reverse=True)[:100])
    print(f"Overlap of top-100 by cone and top-100 by degree: {len(top100_cone & top100_deg)}")
    print("High degree, small cone:", [(a, g.degree(a), cones[a]) for a in sorted(top100_deg - top100_cone, key=g.degree, reverse=True)[:5]])
    print("Large cone, lower degree:", [(a, g.degree(a), cones[a]) for a in sorted(top100_cone - top100_deg, key=cones.get, reverse=True)[:5]], "\n")
    table.to_csv(config.OUT_DIR / "task5_top_cones.csv", index=False)
    pd.Series(cones, name="cone_size").rename_axis("asn").to_csv(config.OUT_DIR / "task5_all_cones.csv")
    plot_graph6(cones)
