from . import config
from .loaders import load_as_types
from .plotting import save


def summarize(df):
    raise NotImplementedError


def plot_graph1(summary_2015, summary_2021):
    raise NotImplementedError


def run():
    t15 = load_as_types(config.TYPES_2015)
    t21 = load_as_types(config.TYPES_2021)
