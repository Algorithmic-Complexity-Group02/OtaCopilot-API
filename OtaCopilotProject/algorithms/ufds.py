
class DSU:
    def __init__(self, nodes):
        self.nodes = list(map(str, nodes))
        self.parent_of = {node: node for node in self.nodes}
        self.rank_of = {node: 1 for node in self.nodes}

    def find(self, node):
        if self.parent_of[node] != node:
            self.parent_of[node] = self.find(self.parent_of[node])
        return self.parent_of[node]

    def union(self, node1, node2):
        if node1 not in self.parent_of or node2 not in self.parent_of:
            return False

        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 == root2:
            return False

        if self.rank_of[root1] >= self.rank_of[root2]:
            self.parent_of[root2] = root1
            self.rank_of[root1] += self.rank_of[root2]
        else:
            self.parent_of[root1] = root2
            self.rank_of[root2] += self.rank_of[root1]

        return True
