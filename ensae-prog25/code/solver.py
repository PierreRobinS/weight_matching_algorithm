import itertools
from collections import deque
from graph import *

class Solver:
    """
    A solver class. 

    Attributes: 
    -----------
    grid: Grid
        The grid
    pairs: list[tuple[tuple[int]]]
        A list of pairs, each being a tuple ((i1, j1), (i2, j2))
    """

    def __init__(self, grid):
        """
        Initializes the solver.

        Parameters: 
        -----------
        grid: Grid
            The grid
        """
        self.grid = grid
        self.pairs = list()

    def __str__(self):
        """
        Thought to display the results of the solver after the run() method present in each was called.
        """
        output = "The pairs found are : \n"
        for pair in self.pairs:
            str_pair = str(pair)
            output += str_pair + "\n"
        output += "\nAnd the score is : " + str(self.score(self.pairs))
        return output

    def score(self, pair_list):
        """
        Computes the score of the given list of pairs.
        If there are some cases that don't match with any others, then it adds the value associated
        """
        S = 0
        involved_cases = list()
        for pair in pair_list:
            S += self.grid.cost(pair)
            for i in range(2):
                involved_cases.append(pair[i])
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if (not (i,j) in involved_cases) and (self.grid.color[i][j] != 4):
                    S += self.grid.value[i][j]
        return S

class SolverEmpty(Solver):
    def run(self):
        pass

class SolverGreedy1(Solver):
    """
    A first very (very) greedy solver that find the best solution to the problem. Complexity about o(2^n)
    
    Works as following:
    - Computes the power set of self.grid.all_pairs()
    - Excludes all subsets of pairs that are illegals. For instance a cell can be 
    involved in two different pairs in the previous powerset.
    - Gets the subset with the lowest score.
    """

    def power_set(self, lst):
        """
        Return a list that is the power set of a given list.
        """
        output = []
        for r in range(len(lst) + 1):
            for i in itertools.combinations(lst, r):
                output.append(list(i))
        return output
    
    def is_legal(self, pair_list):
        """
        This boolean function returns true if the given list of pairs respects the rules of the problem, ie,
        every element of the grid can't be taken in two pairs at the same time.
        
        Parameters:
        -----------
        pair_list : this is a list of tuples of tuples, ie [( (i1,j1), (i2,j2) ), ..., (...)]
        """
        n = self.grid.n
        m = self.grid.m
        for i in range(n):
            for j in range(m):
                pair_involved = 0
                for pair in pair_list:
                    if (i,j) in pair:
                        pair_involved += 1
                if pair_involved >= 2:
                    return False
        return True
    
    def run(self):
        """
        Returns a list of pair with its score associated using a total solving algorithm.

        This last one works as following :
            - Computing all the subsets from the all_pair() list.
            - Takes only the legal ones and rejects the others
            - Sort all the legal lists
        """
        def sort_key(lst):
                return lst[1]
        all_legal_pair_lists = []
        all_pairs = self.grid.all_pairs()
        all_pair_lists = self.power_set(all_pairs)
        for lst in all_pair_lists:
            if self.is_legal(lst) == True:
                all_legal_pair_lists.append((lst, self.score(lst)))
        all_legal_pair_lists.sort(key=sort_key)
        self.pairs = all_legal_pair_lists[0][0]
        return all_legal_pair_lists[0]
    

class SolverGreedy2(Solver):

    def compute_min_dr(self, i, j):
        """
        Computes the best pair from a given cell and its associated cost.

        Returns a tuple (pair, int) whose pair is a tuple (c1,c2) of tuples and int is the cost of this given pair.
        The concerned pair is the one with the smallest cost for a given cell (i,j)

        NB : it looks only the lower and the right cell because of the form of local_pairs_dr() in grid.py
        PROBLEM NOT YET SOLVED : both pairs for a given cell can have the same cost, then compute_min_dr() chooses one pair randomly.
        """
        cell_costs = dict()
        for pair in self.grid.local_pairs_dr(i, j):
            cell_costs[pair] = self.grid.cost(pair)
            min_pair = pair
        for pair in cell_costs.keys():
            if cell_costs[pair] <= cell_costs[min_pair]:
                min_pair = pair
        if cell_costs != {}:
            return (min_pair, cell_costs[min_pair])
        else:
            return None

    def run(self):
        """
        A greedy algorithm to try to solve the posed problem.
        It has some difficulties to find the best solution, but its results are correct and it is very much faster than the total solver.

        It works as following:
        ----------------------
            - First, it chooses a cell.
            - If the cell is black, it goes to the next.
            - Else, if the cell admit pairs, it computes the best pair associated with compute_min_dr()
            - It computes again the best pair with the cell already involved in the former pair.
            # PROBLEM NOT YET SOLVED : both pairs (if they exist) for a given cell can have the same cost, 
            then compute_min_dr() chooses one pair randomly.
                - If there is no second pair, it adds the first one to self.pairs()
                - If both pairs are the same, then there is a match. It adds it to self.pairs()
                # PROBLEM NOT YET SOLVED : if the second cell admit another pair with an equal cost with the former one,
                the code actually chooses the first pair, even if it is not the best option.
                - If not, it runs the algorithm again (recursivity) to find the best pair of the second cell.
            - When one of the two first cases appears, the algorithm marks the cells with the color 5 to do not loop indefinitely.
            (The last steps works bc the color 5 is added to the is_forbidden() method in self.grid.)

        Axes the improve the algorithm:
        -------------------------------
            - Making compute_min_dr() returning both pairs instead of choosing one randomly when they have the same cost.
            - Then creating a memory system to choose between both paths generated by recursivity from both pairs.
            - Solving the second problem by a similar method.
        """
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if self.grid.color[i][j] != 4:
                    # If the cell isn't black, the code continue
                    if self.compute_min_dr(i,j) != None:
                        min_pair_1 = self.compute_min_dr(i,j)
                        min_pair_2 = self.compute_min_dr(min_pair_1[0][1][0], min_pair_1[0][1][1])
                        # If the cell (i,j) admit pairs, it computes the bests pairs
                        if min_pair_2 == None:
                            for cell in min_pair_1[0]:
                                self.grid.color[cell[0]][cell[1]] = 5
                            self.pairs.append(min_pair_1[0])
                        # If there is no second pair, it adds the first one to self.pairs()
                        else:
                            # If there is a second pair.
                            if min_pair_1[1] <= min_pair_2[1]:
                                for cell in min_pair_1[0]:
                                    self.grid.color[cell[0]][cell[1]] = 5
                                self.pairs.append(min_pair_1[0])
                            # When there is a match. (Problem : using the '<=' symbol, the code should separate '=' and '<' cases.)
                            else:
                                self.grid.color[i][j] = 5
                                self.run()
                                # When there is not.
                    else:
                        self.grid.color[i][j] = 5




class SolverFordFulkerson(Solver):
    
    def find_path_BFS(self, residual, source, sink):
        """
        Searches for an augmenting path in the residual graph using BFS.
        Returns a pair (path, parent):
            - path: list of edges in the form [(u, v), ...] going from source to sink,
            or None if no path exists.
            - parent: array indicating for each vertex the predecessor in the found path.
        """
        n = len(residual)
        visited = [False] * n

        parent = [-1] * n
        queue = deque()

        visited[source] = True
        queue.append(source)
        while queue:
            u = queue.popleft()
            for v in range(n):
                if not visited[v] and residual[u][v] > 0:
                    visited[v] = True
                    parent[v] = u
                    queue.append(v)
                    if v == sink:
                        # We have reached the sink; we can reconstruct the path
                        return self.build_path(parent, source, sink), parent
        return None, parent
    
    def build_path(self, parent, source, sink):
        """
        Reconstructs the path from source to sink using the parent array.
        Returns the list of edges [(u, v), ...].
        """
        path = []
        v = sink
        while v != source:
            u = parent[v]
            path.insert(0, (u, v))
            v = u
        return path
    
    def run(self):
        """
        This method runs the algorithm to solve the problem.

        Returns max_flox (int) which is the maximum flow found associated to graph problem.
        The best pair list is stocked in self.pairs().
        """
        grid_graph = BipartiteGraph(self.grid)

        source = grid_graph.n - 2
        sink = grid_graph.n - 1

        residual = [row[:] for row in grid_graph.adj_matrix]
        max_flow = 0

        # Use BFS to find an augmenting path
        while True:
            path, parent = self.find_path_BFS(residual, source, sink)
            if path is None:
                break
            flow = 1  # Unit capacity
            v = sink
            while v != source:
                u = parent[v]
                residual[u][v] -= flow
                residual[v][u] += flow
                v = u
            max_flow += flow

        # Extract pairs from the residual matrix
        # Iterate over the vertices corresponding to cells (0 to grid.n*grid.m - 1)
        for u in range(grid_graph.n - 2):  # excluding source and sink
            # Consider only the vertices of the left part
            # Here, we assume that grid_graph.id_cell[u][0] gives the cell coordinate and
            # that (i+j) even indicates the left part.
            cell_u = grid_graph.id_cell[u][0]
            if (cell_u[0] + cell_u[1]) % 2 == 0:  # left part
                # For each neighbor v of u
                for v in range(grid_graph.n - 2):
                    # Check that we have an initial edge and that this edge has been saturated
                    if grid_graph.adj_matrix[u][v] == 1 and residual[u][v] == 0:
                        cell_v = grid_graph.id_cell[v][0]
                        self.pairs.append((cell_u, cell_v))
                        break  # Each left cell can be paired with only one cell

        return max_flow
