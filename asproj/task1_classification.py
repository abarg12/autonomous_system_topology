import matplotlib.pyplot as plt
import pandas as pd

from . import config
from .loaders import load_as_types
from .plotting import save


def summarize(df):
    counts = df["type"].value_counts().sort_index()
    return pd.DataFrame({"count": counts, "percent": 100 * counts / counts.sum()})


def plot_graph1(summary_2015, summary_2021):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for ax, (year, s) in zip(axes, [(2015, summary_2015), (2021, summary_2021)]):
        bars = ax.bar(s.index, s["count"], color=["tab:orange", "tab:green", "tab:blue"])
        for bar, (c, p) in zip(bars, s[["count", "percent"]].values):
            ax.annotate(f"{int(c):,}\n({p:.1f}%)", (bar.get_x() + bar.get_width() / 2, c), ha="center", va="bottom")
        ax.set_title(f"{year} (N = {int(s['count'].sum()):,} classified ASes)")
        ax.set_xlabel("Business class")
    axes[0].set_ylabel("Number of ASes")
    axes[0].set_ylim(0, max(summary_2015["count"].max(), summary_2021["count"].max()) * 1.2)
    fig.suptitle("Graph 1: CAIDA AS business classification")
    save(fig, "graph1_classification")


def run():
    t15 = load_as_types(config.TYPES_2015)
    t21 = load_as_types(config.TYPES_2021)
    s15, s21 = summarize(t15), summarize(t21)
    change = pd.DataFrame({
        "count_2015": s15["count"], "count_2021": s21["count"],
        "count_change": s21["count"] - s15["count"],
        "pct_2015": s15["percent"].round(2), "pct_2021": s21["percent"].round(2),
        "share_change_pp": (s21["percent"] - s15["percent"]).round(2),
    })
    print("== Task 1: AS classification ==")
    print(f"Total classified: 2015={len(t15):,}  2021={len(t21):,}")
    print(change.to_string(), "\n")
    change.to_csv(config.OUT_DIR / "task1_classification.csv")
    plot_graph1(s15, s21)
