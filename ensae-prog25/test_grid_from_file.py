import sys 
sys.path.append("code/")  # Make sure that the directory "code/" is the one containing your modules

import unittest 
from grid import Grid
from solver import *
from graph import *

# -------------------------------
# Tests for loading and methods of Grid
# -------------------------------
class Test_GridLoading(unittest.TestCase):
    def test_grid0(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]])

    def test_grid0_novalues(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=False)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        # When not reading values, all must be equal to 1
        self.assertEqual(grid.value, [[1, 1, 1], [1, 1, 1]])

    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 4, 3], [2, 1, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [1, 1, 3]])

class Test_GridMethods(unittest.TestCase):
    def setUp(self):
        self.grid = Grid.grid_from_file("input/grid00.in", read_values=True)

    def test_is_forbidden(self):
        # For grid00.in, all cells are white (code 0) so none are forbidden.
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                self.assertFalse(self.grid.is_forbidden(i, j))

    def test_is_peace(self):
        # For grid00.in, all cells are white, so is_peace should return True.
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                self.assertTrue(self.grid.is_peace(i, j))

    def test_cost(self):
        # For a pair ((0,0),(0,1)) : |5 - 8| = 3
        c = self.grid.cost(((0, 0), (0, 1)))
        self.assertEqual(c, 3)

    def test_local_pairs_dr(self):
        # For cell (0,0) in grid00.in, there are potentially 2 pairs: with (0,1) and (1,0)
        pairs = self.grid.local_pairs_dr(0, 0)
        expected = [((0, 0), (0, 1)), ((0, 0), (1, 0))]
        self.assertCountEqual(pairs, expected)

    def test_all_pairs(self):
        pairs = self.grid.all_pairs()
        # For grid00.in, we expect to get several pairs; we simply check that the list is not empty.
        self.assertTrue(len(pairs) > 0)

# -------------------------------
# Tests for the Graph class
# -------------------------------
class Test_Graph(unittest.TestCase):
    def test_add_edge_and_exist(self):
        g = Graph(3)
        g.add_edge(0, 1, 5)
        self.assertTrue(g.exist_edge(0, 1))
        self.assertEqual(g.adj_matrix[0][1], 5)
        self.assertFalse(g.exist_edge(1, 0))

    def test_add_verctice(self):
        g = Graph(2)
        g.add_verctice()
        self.assertEqual(g.n, 3)
        # The new matrix must be 3x3 and filled with zeros for the new elements.
        self.assertEqual(len(g.adj_matrix), 3)
        self.assertEqual(len(g.adj_matrix[0]), 3)

    def test_get_neighbours(self):
        g = Graph(3)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 2, 1)
        neighbours = g.get_neighbours(0)
        self.assertCountEqual(neighbours, [1, 2])

# -------------------------------
# Tests for the BipartiteGraph class
# -------------------------------
class Test_BipartiteGraph(unittest.TestCase):
    def test_bipartite_construction(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        bg = BipartiteGraph(grid)
        # The total number of vertices must be grid.n * grid.m + 2 (for the source and the sink)
        self.assertEqual(bg.n, grid.n * grid.m + 2)
        source = bg.n - 2
        sink = bg.n - 1
        # Check that for each cell, there is an arc to the source or the sink depending on the parity of (i+j)
        for (cell, k) in bg.id_cell:
            if (cell[0] + cell[1]) % 2 == 0:
                self.assertEqual(bg.adj_matrix[source][k], 1)
            else:
                self.assertEqual(bg.adj_matrix[k][sink], 1)

# -------------------------------
# Tests for the solvers
# -------------------------------
class Test_SolverGreedy1(unittest.TestCase):
    def test_solver_greedy1(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        solver = SolverGreedy1(grid)
        result = solver.run()
        # The run of SolverGreedy1 returns a tuple (list of pairs, score)
        pair_list, score = result
        # Check that each cell is used only once
        used_cells = set()
        for pair in pair_list:
            for cell in pair:
                self.assertNotIn(cell, used_cells)
                used_cells.add(cell)
        # Check that the returned score matches the one calculated by the score method
        computed_score = solver.score(pair_list)
        self.assertEqual(score, computed_score)

class Test_SolverFordFulkerson(unittest.TestCase):
    def test_solver_ford_fulkerson(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        solver = SolverFordFulkerson(grid)
        max_flow = solver.run()
        # For grid00.in, with 2 rows and 3 columns, we expect a matching of 3 pairs.
        self.assertEqual(max_flow, 3)
        # Check that the number of pairs found is correct
        self.assertEqual(len(solver.pairs), 3)
        # Check that each cell appears at most in one pair
        used_cells = set()
        for pair in solver.pairs:
            for cell in pair:
                self.assertNotIn(cell, used_cells)
                used_cells.add(cell)

# -------------------------------
# Running the tests
# -------------------------------
if __name__ == '__main__':
    unittest.main()
