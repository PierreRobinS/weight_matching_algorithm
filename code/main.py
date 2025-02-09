from grid import Grid
from solver import *
import os
import numpy as np
import matplotlib.pyplot as plt

import os

# Change le répertoire de travail au répertoire contenant le script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

data_path = "../input/"

file_name = data_path + "grid00.in"
grid = Grid.grid_from_file(file_name, True)
print(grid)
solver = SolverGreedyEasy(grid)
solver.run_real()
print("liste de paires : ", solver.pairs, "\n", "score : ", solver.score(solver.pairs))

"""file_name = data_path + "grid11.in"
grid = Grid.grid_from_file(file_name, read_values=True)
print(grid)
solver = SolverTotal(grid)
#print("The final score of SolverEmpty is:", solver.run())
"""