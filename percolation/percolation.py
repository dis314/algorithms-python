from weighted_quick_union import WeightedQuickUnionPS
from random import randrange
import math
import matplotlib as mpl
import matplotlib.cm as cmx
import matplotlib.pyplot as plt



class Percolation:

    def __init__(self, n):
        self.grid = self.create_grid(n)
        self.dim = n
        self.wqu = WeightedQuickUnionPS(n)

    def create_grid(self, n):
        grid = []
        for i in range(n):
            row = []
            for j in range(n):
                # nums = [random.randint(0, 100) for i in range(n*n)]
                # opens = [True if i>=100-t else False for i in nums]
                # row.append(random.randint(0, 100))
                row.append(0)
            grid.append(row)
            # grid2 = map(lambda x: [1 if i>=100-t else 0 for i in x], grid)
        return grid

    def open(self, row, col):
        if self.grid[row][col] != 1:
            self.grid[row][col] = 1

    def is_open(self, row, col):
        return self.grid[row][col]

    def is_full(self, row, col):
        pass

    def count_open(self):
        opensites = 0
        for row in self.grid:
            for item in row:
                opensites += item
        return opensites

    def percolates(self):
        grid = self.grid
        n = self.dim
        for i in range(n):
            for j in range(n):
                if self.is_open(i, j):
                    try:
                        if self.is_open(i, j+1):
                            # if not(wqu.connected(self.grid[i, j], self.grid[i+1, j])):
                            self.wqu.union(i*n+j, i*n+j+1)
                    except IndexError:
                        pass

                    try:
                        if self.is_open(i+1, j):
                            p = i*n+j
                            q = (i+1)*n+j
                            self.wqu.union(p, q)
                    except IndexError:
                        pass
        perc = False
        for i in range(n):
            for j in range(n):
                if self.wqu.connected(self.wqu.sitelist[i], self.wqu.sitelist[n*n-n+j]):
                    return True
        return perc

    def main(self):
        # nums = [random.randint(0, 100) for i in range(self.dim)]
        # opens = [True if i>=100-t else False for i in nums]
        pass

class PercolationStats:

    def __init__(self, n, T):
        self.dimension = int(n)
        self.ntrials = int(T)
        self.mean = float()
        self.std = float()
        self.tables = []

    def stddev(self, *args):
        pass

    def confidence_high(self, *args):
        pass

    def confidence_low(self, *args):
        pass

    def plot(self):
        print('\nComputing for plotting...')
        prob = [i for i in range(100)]
        N = self.dimension
        is_perc = []
        test_dict = {}
        for t in range(self.ntrials):
            is_perc = {}
            for p in prob:
                count = 0
                table = Percolation(N)
                exclude = ()
                while count <= N*N*p*0.01:
                    site_ind = (randrange(0,N),randrange(0,N))
                    if site_ind not in exclude:
                        exclude += (site_ind)
                        if not(table.is_open(*site_ind)):
                            table.open(*site_ind)
                            count += 1
                            # print('Opened: ', count)
                # print('Percent: ', p)
                is_perc[p] = table.percolates()
            print('Trial №', t)
            test_dict[t] = is_perc
        data = {}
        for i in range(100):
            data[i] = 0

        for key,val in test_dict.items():
            prob = []
            for k,v in val.items():
                prob.append(int(v))
                data[k] = data[k] + prob[k]
        for key in data:
            data[key] = data[key]/self.ntrials

        x, y = zip(*data.items())
        fig, ax = plt.subplots(1, 1)
        plt.plot(x, y)
        plt.show()
        return print('Done!')

    def plot_grid(self, grid):

        fig, ax = plt.subplots(1, 1, tight_layout=True)
        for x in range(n+1):
            ax.axhline(x, lw=2, color='k', zorder=5)
            ax.axvline(x, lw=2, color='k', zorder=5)

        cmap = cmx.Purples
        ax.imshow(grid, interpolation='none', cmap=cmap, extent=[0, n, 0, n], zorder=0)
        ax.axis('off')
        plt.show()

    def main(self):
        n = self.dimension
        ntrials = self.ntrials
        results = []
        count = 0

        for i in range(ntrials):
            table = Percolation(n)
            count = 0
            while not(table.percolates()):
                site_ind = (randrange(0,n),randrange(0,n))
                count += 1
                if not(table.is_open(*site_ind)):
                    table.open(*site_ind)
                else:
                    continue
            print('Test {}: completed; opened: {}; number of operations: {}'.format(i, table.count_open(), count))
            self.tables.append(table.grid)
            results.append(table.count_open()/(n*n))

        self.mean = sum(results)/float(len(results))
        s = float()
        for x in results:
            s += (x-self.mean)**2
        s = s/(ntrials-1)
        self.std = math.sqrt(s)
        
        return results
        
if __name__ == "__main__":
    print('''\nDue to time consuming nature of this algorithm
it is recommended to set dimesion < 100 and trials < 50\n''')
    n = input('Enter dimension: ')
    T = input('Enter number of trials: ')
    simulation = PercolationStats(n, T)
    res = simulation.main()
    print('Mean: ', '%.3f'%simulation.mean)
    print('Std: ', '%.3f'%simulation.std)
    simulation.plot()
