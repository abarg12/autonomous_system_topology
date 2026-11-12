import matplotlib.pyplot as plt
import pandas as pd

from . import config
from .plotting import save

ROLES = ["Customer-serving", "Peering edge", "Stub/Multi-homed"]


def structural_role(g, asn):
    if g.customer_degree(asn) > 0:
        return ROLES[0]
    if g.peer_degree(asn) > 0:
        return ROLES[1]
    return ROLES[2]


def contingency_table(types_df, g):
    nodes = set(g.nodes)
    matched = types_df[types_df["asn"].isin(nodes)].copy()
    matched["role"] = matched["asn"].map(lambda a: structural_role(g, a))
    print(f"Classified ASes: {len(types_df):,}  graph ASes: {len(nodes):,}")
    print(f"Matched: {len(matched):,}  classified-only (excluded): {len(types_df) - len(matched):,}  "
          f"graph-only (excluded): {len(nodes) - len(matched):,}")
    return pd.crosstab(matched["type"], matched["role"]).reindex(columns=ROLES, fill_value=0), matched


def plot_graph5(table):
    pct = table.div(table.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(8, 5))
    bottom = pd.Series(0.0, index=pct.index)
    for role in ROLES:
        ax.bar(pct.index, pct[role], bottom=bottom, label=role)
        for i, (b, v) in enumerate(zip(bottom, pct[role])):
            if v > 3:
                ax.text(i, b + v / 2, f"{v:.1f}%", ha="center", va="center", fontsize=9)
        bottom += pct[role]
    ax.set_xticks(range(len(pct)), [f"{t}\n(n = {n:,})" for t, n in table.sum(axis=1).items()])
    ax.set_ylabel("% of ASes in business class")
    ax.set_xlabel("Business class (2021)")
    ax.set_title("Graph 5: Structural role by business class (2024 graph)")
    ax.legend(bbox_to_anchor=(1, 1), loc="upper left")
    save(fig, "graph5_roles")


def run(g, types_df):
    print("== Task 4: Business vs structural roles ==")
    table, matched = contingency_table(types_df, g)
    print(table.to_string())
    print((table.div(table.sum(axis=1), axis=0) * 100).round(1).to_string(), "\n")
    table.to_csv(config.OUT_DIR / "task4_contingency.csv")
    for t, role in [("Enterprise", ROLES[0]), ("Content", ROLES[2]), ("Transit/Access", ROLES[2])]:
        ex = matched[(matched["type"] == t) & (matched["role"] == role)]["asn"]
        ex = sorted(ex, key=g.degree, reverse=True)[:3]
        print(f"{t} + {role} examples:", [(a, g.degree(a), g.customer_degree(a)) for a in ex])
    print()
    plot_graph5(table)
