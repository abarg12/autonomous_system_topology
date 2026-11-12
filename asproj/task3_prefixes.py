import ipaddress

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import config
from .plotting import save


def merge_intervals(intervals):
    total, cur_start, cur_end = 0, None, None
    for start, end in sorted(intervals):
        if cur_end is None or start > cur_end:
            if cur_end is not None:
                total += cur_end - cur_start
            cur_start, cur_end = start, end
        else:
            cur_end = max(cur_end, end)
    if cur_end is not None:
        total += cur_end - cur_start
    return total


def to_intervals(pfx_df):
    start = pfx_df["prefix"].map(lambda p: int(ipaddress.IPv4Address(p)))
    return pfx_df.assign(start=start, end=start + 2 ** (32 - pfx_df["length"]))


def per_as_stats(pfx_df):
    """DataFrame: asn, num_prefixes (P_i), num_addresses (A_i)"""
    df = to_intervals(pfx_df).explode("origins").rename(columns={"origins": "asn"})
    rows = [
        (asn, len(grp), merge_intervals(zip(grp["start"], grp["end"])))
        for asn, grp in df.groupby("asn")
    ]
    return pd.DataFrame(rows, columns=["asn", "num_prefixes", "num_addresses"])


def check_merge():
    assert merge_intervals([(0, 65536), (256, 512)]) == 65536
    assert merge_intervals([(0, 256), (256, 512), (1024, 1280)]) == 768
    assert merge_intervals([(0, 256), (0, 256)]) == 256
    print("merge_intervals sanity checks passed")


def plot_graph4(stats_df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for ax, col, label, name in [
        (axes[0], "num_prefixes", "Prefixes per AS, $P_i$", "4a"),
        (axes[1], "num_addresses", "Unique IPv4 addresses per AS, $A_i$", "4b"),
    ]:
        v = stats_df[col]
        bins = np.logspace(0, np.log10(v.max()) + 0.1, 40)
        ax.hist(v, bins=bins)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel(label + " (log bins)")
        ax.set_ylabel("Number of origin ASes")
        ax.set_title(f"Graph {name}")
    fig.suptitle(f"Graph 4: IPv4 prefix and address distributions (N = {len(stats_df):,} origin ASes)")
    fig.tight_layout()
    save(fig, "graph4_prefixes_addresses")


def run(pfx_df):
    print("== Task 3: Prefixes ==")
    check_merge()
    multi = pfx_df["origins"].map(len) > 1
    print(f"Distinct prefixes: {len(pfx_df):,}  multi-origin: {multi.sum():,}")
    iv = to_intervals(pfx_df)
    global_union = merge_intervals(zip(iv["start"], iv["end"]))
    print(f"Global union of addresses: {global_union:,} ({100 * global_union / 2**32:.1f}% of IPv4)")
    print(f"Sum of raw prefix sizes (with overlaps): {int((iv['end'] - iv['start']).sum()):,}")

    stats = per_as_stats(pfx_df)
    stats["addr_per_prefix"] = stats["num_addresses"] / stats["num_prefixes"]
    assert (stats["num_addresses"] <= stats["num_prefixes"] * 2**24).all()
    print(f"Origin ASes: {len(stats):,}")
    print(stats[["num_prefixes", "num_addresses"]].describe().to_string())
    print("Top by prefix count:")
    print(stats.sort_values("num_prefixes", ascending=False).head(10).to_string(index=False))
    print("Top by address count:")
    print(stats.sort_values("num_addresses", ascending=False).head(10).to_string(index=False), "\n")
    stats.to_csv(config.OUT_DIR / "task3_per_as.csv", index=False)
    plot_graph4(stats)
