import pandas as pd


def load_as_types(path) -> pd.DataFrame:
    """Columns: asn, source, type"""
    raise NotImplementedError


def load_as_rel(path) -> pd.DataFrame:
    """Columns: as1, as2, rel  (rel -1 = as1 provider of as2, 0 = peers)"""
    raise NotImplementedError


def load_pfx2as(path) -> pd.DataFrame:
    """Columns: prefix, length, origins (list of ASNs)"""
    raise NotImplementedError


def load_as_org(path) -> dict[int, str]:
    """ASN -> organization name"""
    raise NotImplementedError
