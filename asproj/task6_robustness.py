from .plotting import save

FRACTIONS = [0, 0.01, 0.02, 0.05, 0.10]
TRIALS = 10


def surviving_fraction(g, removed):
    raise NotImplementedError


def random_removal(g, f, seed):
    raise NotImplementedError


def targeted_removal(g, f):
    raise NotImplementedError


def plot_robustness(random_results, targeted_results):
    raise NotImplementedError


def run(g):
    pass
