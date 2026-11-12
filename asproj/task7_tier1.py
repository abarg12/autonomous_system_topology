import pandas as pd

from . import config


def greedy_clique(g, max_rank=50):
    ranked = sorted(g.nodes, key=g.degree, reverse=True)[:max_rank]
    clique, skipped = [ranked[0]], []
    for a in ranked[1:]:
        if all(c in g.neighbors[a] for c in clique):
            clique.append(a)
        else:
            skipped.append(a)
    return clique, skipped


def tier1_table(g, clique, orgs, n=10):
    return pd.DataFrame({
        "order": range(1, min(n, len(clique)) + 1),
        "asn": clique[:n],
        "organization": [orgs.get(a, "") for a in clique[:n]],
        "degree": [g.degree(a) for a in clique[:n]],
    })


def run(g, orgs):
    print("== Task 7: Tier-1 clique ==")
    clique, skipped = greedy_clique(g)
    print(f"Clique size (top 50 by degree): {len(clique)}")
    print(f"Skipped (not connected to all of S): {skipped}")
    table = tier1_table(g, clique, orgs)
    print(table.to_string(index=False), "\n")
    table.to_csv(config.OUT_DIR / "task7_tier1.csv", index=False)
