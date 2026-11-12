import pandas as pd


def load_as_types(path) -> pd.DataFrame:
    """Columns: asn, source, type"""
    df = pd.read_csv(path, sep="|", comment="#", header=None, names=["asn", "source", "type"])
    df = df.dropna().drop_duplicates()
    df["asn"] = df["asn"].astype(int)
    return df.drop_duplicates("asn")


def load_as_rel(path) -> pd.DataFrame:
    """Columns: as1, as2, rel  (rel -1 = as1 provider of as2, 0 = peers)"""
    df = pd.read_csv(path, sep="|", comment="#", header=None, names=["as1", "as2", "rel", "source"])
    df = df.dropna(subset=["as1", "as2", "rel"]).astype({"as1": int, "as2": int, "rel": int})
    df = df[df["rel"].isin([-1, 0]) & (df["as1"] != df["as2"])]
    key = df[["as1", "as2"]].min(axis=1).astype(str) + "-" + df[["as1", "as2"]].max(axis=1).astype(str)
    return df.loc[~key.duplicated(), ["as1", "as2", "rel"]].reset_index(drop=True)


def load_pfx2as(path) -> pd.DataFrame:
    """Columns: prefix, length, origins (list of ASNs)"""
    df = pd.read_csv(path, sep="\t", header=None, names=["prefix", "length", "origins"], dtype=str)
    df = df.dropna().drop_duplicates(["prefix", "length"])
    df["length"] = df["length"].astype(int)
    df["origins"] = df["origins"].str.replace(",", "_").str.split("_").map(lambda xs: sorted({int(x) for x in xs}))
    return df.reset_index(drop=True)


def load_as_org(path) -> dict[int, str]:
    """ASN -> organization name"""
    org_names, as_org = {}, {}
    section = None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("# format:org_id"):
                section = "org"
            elif line.startswith("# format:aut"):
                section = "aut"
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("|")
            if section == "org" and len(parts) >= 3:
                org_names[parts[0]] = parts[2]
            elif section == "aut" and len(parts) >= 4 and parts[0].isdigit():
                as_org[int(parts[0])] = parts[3]
    return {asn: org_names.get(org, "") for asn, org in as_org.items()}
