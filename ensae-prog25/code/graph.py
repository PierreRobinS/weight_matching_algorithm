import matplotlib.pyplot as plt
from random import *
import grid

class Graph:
    """
    A class that enable to represent a graph in a adjency matrix.
    """
    def __init__(self, n):
        """
        Input:
        ------
        n : the number of verctices we want in the graph.
        """
        self.n = n
        self.adj_matrix = [[0]*n for _ in range(n)]

    def __str__(self):
        """
        Prints the adjency matrix of the graph.
        """
        output = f"The graph adjency matrix is {self.n} x {self.n} sized and is :\n"
        for i in range(self.n): 
            output += f"{[self.adj_matrix[i][j] for j in range(self.n)]}\n"
        return output

    def add_verctice(self):
        """
        Adds a verctice to the graph.
        In facts, we up the size of the ajdcency matrix with 1 row and 1 column.
        """
        self.n += 1
        for l in self.adj_matrix:
            l.append(0)
        self.adj_matrix.append([0]*self.n)

    def add_edge(self, s, e, p=1):
        """
        Adds an edge to the graph between the verctices s and e.
        p can be a ponderation value.
        """
        self.adj_matrix[s][e] = p

    def exist_edge(self, s, e):
        """
        Returns True if the edge between e and s exists and Fasle otherwise.
        """
        return bool(self.adj_matrix[s][e])
    
    def get_neighbours(self, s):
        """
        Returns a list of tuples(int) that represents all the neighbours of a given verctice.
        """
        neighbours = []
        for i in range(self.n):
            if self.adj_matrix[s][i] != 0:
                neighbours.append(i)
        return neighbours
    

class BipartiteGraph(Graph):
    """
    A class that represents a bipartite graph specialized to solve the Maximum Flow Problem.
    This class is also thought to convert grids in graph in a simple way.
    """

    def __init__(self, grid):
        """
        Initializating a bipartite graph from a given grid.

        Each cell is attributed an identifaction number k which tie this cell with a precise verctice of the graph.
        If a cell is pair, ie i+j is pair, then it is tied to the source.
        Else, it is tied to the sink.
        If there is a pair between two cell, then an edge is added between both associated verctices.
        """
        super().__init__(grid.n*grid.m+2)
        all_pairs = grid.all_pairs()
        k = 0
        id_cell = []
        # Setting up the sink and the source
        for i in  range(grid.n):
            for j in range(grid.m):
                id_cell.append(((i,j), k))
                if (i+j)%2==0:
                    self.add_edge(self.n-2, k)
                else:
                    self.add_edge(k, self.n-1) 
                k += 1
        self.id_cell = id_cell
        # Adding edges between cells that admit pairs
        for t in id_cell:
            for pair in all_pairs:
                if t[0] == pair[0]:
                    for t_mate in id_cell:
                        if t_mate[0] == pair[1]:
                            if (t[0][0] + t[0][1]) % 2 == 0:
                                self.add_edge(t[1], t_mate[1])
                            else:
                                self.add_edge(t_mate[1], t[1])
        #print(self)

    def plot(self):
        """
        Plots the graph of the grid.
        """
        for i in range(self.n-2):
            if self.exist_edge(i, self.n-1):
                plt.plot([0, 1], [(self.n-3)/2, i], marker='o', color='black')
                for j in range(self.n-2):
                    if self.exist_edge(i,j):
                        plt.plot([1, 2], [i, j], marker='o', color='black')
            else:
                plt.plot([3, 2], [(self.n-3)/2, i], marker='o', color='black')
                for j in range(self.n-2):
                    if self.exist_edge(i,j):
                        plt.plot([2, 1], [i, j], marker='o', color='black')
        plt.show()

    



    



    
