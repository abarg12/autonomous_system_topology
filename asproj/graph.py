from collections import defaultdict


class ASGraph:
    def __init__(self, rel_df):
        self.customers = defaultdict(set)
        self.providers = defaultdict(set)
        self.peers = defaultdict(set)
        self.neighbors = defaultdict(set)
        self._build(rel_df)

    def _build(self, rel_df):
        raise NotImplementedError

    @property
    def nodes(self):
        return self.neighbors.keys()

    def degree(self, asn):
        return len(self.neighbors[asn])

    def customer_degree(self, asn):
        return len(self.customers[asn])

    def peer_degree(self, asn):
        return len(self.peers[asn])

    def provider_degree(self, asn):
        return len(self.providers[asn])
