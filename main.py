import argparse

from asproj import config
from asproj.graph import ASGraph
from asproj.loaders import load_as_rel, load_as_types, load_pfx2as, load_as_org
from asproj import (
    task1_classification,
    task2_degrees,
    task3_prefixes,
    task4_roles,
    task5_cones,
    task6_robustness,
    task7_tier1,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tasks", nargs="*", type=int, default=list(range(1, 8)))
    tasks = set(parser.parse_args().tasks)
    config.OUT_DIR.mkdir(exist_ok=True)

    if 1 in tasks:
        task1_classification.run()

    g = ASGraph(load_as_rel(config.AS_REL)) if tasks & {2, 4, 5, 6, 7} else None
    orgs = load_as_org(config.AS_ORG) if tasks & {5, 7} else None

    if 2 in tasks:
        task2_degrees.run(g)
    if 3 in tasks:
        task3_prefixes.run(load_pfx2as(config.PFX2AS))
    if 4 in tasks:
        task4_roles.run(g, load_as_types(config.TYPES_2021))
    if 5 in tasks:
        task5_cones.run(g, orgs)
    if 6 in tasks:
        task6_robustness.run(g)
    if 7 in tasks:
        task7_tier1.run(g, orgs)


if __name__ == "__main__":
    main()
