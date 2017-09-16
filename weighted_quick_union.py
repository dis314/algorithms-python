class WeightedQuickUnionPS:

    def __init__(self, n):
        self.sitelist = [i for i in range(n*n)]
        self.size = [1]*n*n
        self.count = len(self.sitelist)

    def root(self, i):
        while i != self.sitelist[i]:
            self.sitelist[i] = self.sitelist[self.sitelist[i]]
            i = self.sitelist[i]
        return i

    def union(self, p, q):
        i = self.root(p)
        j = self.root(q)

        if i == j:
            return
        if self.size[i] <= self.size[j]:
            self.sitelist[i] = j
            self.size[j] += self.size[i]
        else:
            self.sitelist[j] = i
            self.size[i] += self.size[j]
        self.count -= 1

    def connected(self, p, q):
        return self.root(p) == self.root(q)
