from collections import defaultdict


class ASGraph:
    def __init__(self, rel_df):
        self.customers = defaultdict(set)
        self.providers = defaultdict(set)
        self.peers = defaultdict(set)
        self.neighbors = defaultdict(set)
        self._build(rel_df)

    def _build(self, rel_df):
        for a, b, rel in rel_df[["as1", "as2", "rel"]].itertuples(index=False):
            if rel == -1:
                self.customers[a].add(b)
                self.providers[b].add(a)
            else:
                self.peers[a].add(b)
                self.peers[b].add(a)
            self.neighbors[a].add(b)
            self.neighbors[b].add(a)

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
