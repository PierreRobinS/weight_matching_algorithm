from grid import Grid
from solver import *

import os

# Change the working directory to the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)



data_path = "../input/"
file_name = data_path + "grid13.in"
grid = Grid.grid_from_file(file_name, True)

grid.plot()
#graph = SSBipartiteGraph(grid)
#graph.plot()

solver = SolverFordFulkerson(grid) # Or SolverBruteForce, SolverGreedy, SolverFordFulkerson
solver.run()
print(solver)