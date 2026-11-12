import matplotlib.pyplot as plt

from .config import OUT_DIR


def save(fig, name):
    OUT_DIR.mkdir(exist_ok=True)
    fig.savefig(OUT_DIR / f"{name}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
