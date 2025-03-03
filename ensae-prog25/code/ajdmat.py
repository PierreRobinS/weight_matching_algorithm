from grid import *
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)



class AdjencyMatrix():
    
    def __init__(self, n, m, grid):
        """
        
        
        """
        self.p = n*m

        self.id_cell = list()
        k = 0
        for i in range(n):
            for j in range(m):
                self.id_cell.append(((i,j), k))
                k += 1
        
        self.matrix = [[None]*self.p for _ in range(self.p)]
        all_pairs = grid.all_pairs()
        for cell_1 in self.id_cell:
            for cell_2 in self.id_cell:
                if (cell_1[0], cell_2[0]) in all_pairs:
                    self.matrix[cell_1[1]][cell_2[1]] = grid.cost((cell_1[0], cell_2[0]))
        for l in range(k):
            self.matrix[l][l] = grid.value[self.id_cell[l][0][0]][self.id_cell[l][0][1]]

        for line in self.matrix:
            print(line, "\n")


if __name__ == "__main__":
    grid = Grid.grid_from_file("../input/grid01.in", True)
    ajdmat = AdjencyMatrix(grid.n, grid.m, grid)
