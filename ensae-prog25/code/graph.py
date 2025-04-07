import matplotlib.pyplot as plt
from random import *
from grid import *

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

class Graph:
    """
    A class that enables to represent a graph with an adjacency list.

    Parameters :
    ------------
    n : the number of vertices in the graph.

    adj_list : list of dictionaries (one dictionary per vertex),
        where each dictionary maps a neighbor to the weight (p).
        Example: adj_list[s][e] = p  means there is an edge s -> e with weight p.
    """
    def __init__(self, n):
        """
        Input:
        ------
        n : the number of vertices we want in the graph.
        """
        self.n = n
        # Pour respecter au maximum la structure de la classe d'origine,
        # on garde le nom 'adj_matrix', même si c'est maintenant une liste de dictionnaires.
        self.adj_list = [dict() for _ in range(n)]

    def __str__(self):
        """
        Prints the adjacency representation of the graph.
        """
        output = f"The graph adjacency list with {self.n} vertices is:\n"
        for i in range(self.n):
            # Chaque sommet i a un dictionnaire adj_list[i] de la forme {voisin: poids, ...}
            # On l'affiche sous forme de liste (voisin, poids)
            neighbors_str = ", ".join(f"{k}(p={v})" for k,v in self.adj_list[i].items())
            output += f"Vertex {i} -> [{neighbors_str}]\n"
        return output

    def add_verctice(self):
        """
        Adds a vertex to the graph.
        In fact, we increment the number of vertices and add a new empty dictionary for its adjacency.
        """
        self.n += 1
        self.adj_list.append(dict())

    def add_edge(self, s, e, p=1):
        """
        Adds an edge to the graph between the vertices s and e.
        p can be a weight or capacity value.
        """
        self.adj_list[s][e] = p
        self.adj_list[e][s] = p

    def exist_edge(self, s, e):
        """
        Returns True if the edge between e and s exists, and False otherwise.
        """
        return e in self.adj_list[s]
    
    def get_neighbours(self, s):
        """
        Returns a list of all the neighbors of a given vertex s.
        """
        return list(self.adj_list[s].keys())


class SSBipartiteGraph(Graph):
    """
    A class that represents a bipartite graph specialized to solve the Maximum Flow Problem.
    This class is also thought to convert grids to graphs in a simple way.
    """

    def __init__(self, grid):
        """
        Initializing a bipartite graph from a given grid.

        Each cell is given an identification number k which ties this cell with a precise vertex of the graph.
        If a cell is even (i+j is even), then it is tied to the source (vertex n-2).
        Otherwise, it is tied to the sink (vertex n-1).
        Edges are added between vertices corresponding to cells that are adjacent in the grid.
        """
        # On utilise exactement la même logique que dans la version matrice,
        # mais maintenant, les edges seront stockées sous forme de liste de voisins.
        super().__init__(grid.n * grid.m + 2)  # +2 pour la source et le sink
        all_pairs = grid.all_pairs()
        k = 0
        id_cell = []
        left_vertices = []
        right_vertices = []

        # Setting up source (n-2) and sink (n-1)
        for i in range(grid.n):
            for j in range(grid.m):
                id_cell.append(((i, j), k))
                if (i + j) % 2 == 0:
                    # Sommet associé à la source
                    self.add_edge(self.n - 2, k)
                else:
                    # Sommet associé au sink
                    self.add_edge(k, self.n - 1)
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

    def plot(self):
        """
        Plots the graph of the grid (very schematic).
        """
        for i in range(self.n - 2):
            # Si c'est un sommet qui va vers le sink
            if self.exist_edge(i, self.n - 1):
                plt.plot([0, 1], [(self.n - 3) / 2, i], marker='o')
                for j in range(self.n - 2):
                    if self.exist_edge(i, j):
                        plt.plot([1, 2], [i, j], marker='o')
            else:
                # Sinon, c'est un sommet qui reçoit depuis la source
                plt.plot([3, 2], [(self.n - 3) / 2, i], marker='o')
                for j in range(self.n - 2):
                    if self.exist_edge(i, j):
                        plt.plot([2, 1], [i, j], marker='o')
        plt.show()

if __name__ == "__main__":
    grid = Grid.grid_from_file("../input/grid01.in", True)
    ajdmat = SSBipartiteGraph(grid)
    print(grid)
    print(ajdmat)
    print(ajdmat.adj_list)
    ajdmat.plot()