from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "output"

TYPES_2015 = DATA_DIR / "20150801.as2types.txt"
TYPES_2021 = DATA_DIR / "20210401.as2types.txt"
AS_REL = DATA_DIR / "20241101.as-rel2.txt"
PFX2AS = DATA_DIR / "routeviews-rv2-20251110-1200.pfx2as"
AS_ORG = DATA_DIR / "20251001.as-org2info1.txt"

SEED = 578
