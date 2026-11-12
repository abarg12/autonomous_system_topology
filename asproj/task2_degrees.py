from .plotting import save

BINS = [(0, 0), (1, 1), (2, 5), (6, 100), (101, 500), (501, 1000), (1001, None)]


def degree_table(g):
    """DataFrame: asn, degree, customers, peers, providers"""
    raise NotImplementedError


def validate_identity(deg_df):
    raise NotImplementedError


def plot_graph2_histograms(deg_df):
    raise NotImplementedError


def plot_graph3_ccdf(deg_df):
    raise NotImplementedError


def summary_stats(deg_df):
    raise NotImplementedError


def top_degree(deg_df, n=10):
    raise NotImplementedError


def run(g):
    pass
