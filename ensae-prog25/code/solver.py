import itertools
from collections import deque
from graph import *
from hungarian import *

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

# ------------------------------------------------------------------
# A Brute Force Method
# ------------------------------------------------------------------

class SolverBruteForce(Solver):
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
    
# ------------------------------------------------------------------
# A greedy Method
# ------------------------------------------------------------------

class SolverGreedy(Solver):

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

# ------------------------------------------------------------------
# Ford-Fulkerson Method
# ------------------------------------------------------------------

class SolverFordFulkerson(Solver):
    """
    Solver class that builds a bipartite graph from a grid, computes a maximum matching 
    using the Ford-Fulkerson algorithm (via Edmonds-Karp BFS), and stores the matching 
    pairs in the 'pairs' attribute.
    """

    def __init__(self, grid):
        """
        Initializes the solver with a given grid.

        Args:
            grid: The grid data structure from which the bipartite graph is constructed.
        """
        super().__init__(grid)

    def run(self):
        """
        Executes the matching algorithm. The method performs the following steps:
        
        1. Builds the bipartite graph from the grid and initializes the capacity and 
           residual graphs.
        2. Uses BFS to repeatedly find augmenting paths and updates the residual graph.
        3. Extracts the saturated edges (i.e., those used in the matching) from the flow.
        4. Converts the saturated edges into grid cell pairs and stores the result in 
           the 'pairs' attribute.
        """
        self.G = SSBipartiteGraph(self.grid)
        self.source = self.G.n - 2  # Source vertex
        self.sink = self.G.n - 1    # Sink vertex

        self.capacity, self.residual = self._initialize_graphs()

        while True:
            path = self._bfs_find_path()
            if path is None:
                break
            self._update_flow(path)

        used_edges = self._extract_used_edges()
        self.pairs = self._convert_edges_to_pairs(used_edges)

    def _initialize_graphs(self):
        """
        Initializes the capacity and residual graphs for the bipartite graph.
        Each edge is initialized with capacity 1.

        Returns:
            tuple: Two lists of dictionaries representing the capacity and residual 
                   graphs, respectively.
        """
        n = self.G.n
        capacity = [dict() for _ in range(n)]
        residual = [dict() for _ in range(n)]
        for u in range(n):
            for v, cap in self.G.adj_list[u].items():
                capacity[u][v] = cap
                residual[u][v] = cap
                if u not in residual[v]:
                    residual[v][u] = 0
        return capacity, residual

    def _bfs_find_path(self):
        """
        Performs a breadth-first search on the residual graph to find an augmenting path 
        from the source to the sink.

        Returns:
            list or None: A list of node indices representing the augmenting path if found;
                          otherwise, None.
        """
        visited = [False] * self.G.n
        parent = [-1] * self.G.n

        queue = deque([self.source])
        visited[self.source] = True

        while queue:
            u = queue.popleft()
            for v in self.residual[u]:
                if self.residual[u][v] > 0 and not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    if v == self.sink:
                        return self._reconstruct_path(parent)
                    queue.append(v)
        return None

    def _reconstruct_path(self, parent):
        """
        Reconstructs the augmenting path from the source to the sink using parent pointers.

        Args:
            parent (list): List of parent pointers for each node in the graph.

        Returns:
            list: The augmenting path as a list of node indices.
        """
        path = []
        cur = self.sink
        while cur != self.source:
            path.append(cur)
            cur = parent[cur]
        path.append(self.source)
        path.reverse()
        return path

    def _update_flow(self, path):
        """
        Updates the residual graph along the given augmenting path by reducing the capacity 
        in the forward direction and increasing it in the reverse direction.

        Args:
            path (list): A list of node indices representing the augmenting path.
        """
        flow = min(self.residual[path[i]][path[i+1]] for i in range(len(path) - 1))
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            self.residual[u][v] -= flow
            self.residual[v][u] += flow

    def _extract_used_edges(self):
        """
        Extracts edges from the original graph that have been fully saturated (i.e., used 
        in the matching). Edges directly connected to the source or sink are ignored.

        Returns:
            list: A list of tuples (u, v) representing edges that are part of the matching.
        """
        used_edges = []
        for u in range(self.G.n):
            if u in (self.source, self.sink):
                continue
            for v in self.capacity[u]:
                if v in (self.source, self.sink):
                    continue
                if self.capacity[u][v] == 1 and self.residual[u][v] == 0:
                    used_edges.append((u, v))
        return used_edges

    def _convert_edges_to_pairs(self, used_edges):
        """
        Converts saturated edges into corresponding grid cell pairs using the mapping 
        stored in 'G.id_cell'.

        Args:
            used_edges (list): List of tuples (u, v) representing saturated edges.

        Returns:
            list: List of tuples ((i1, j1), (i2, j2)) representing matching pairs of cells.
        """
        pairs = []
        for u, v in used_edges:
            cell_u = cell_v = None
            for (coords, index) in self.G.id_cell:
                if index == u:
                    cell_u = coords
                elif index == v:
                    cell_v = coords
                if cell_u is not None and cell_v is not None:
                    break
            if cell_u and cell_v:
                pairs.append((cell_u, cell_v))
        return pairs

# ------------------------------------------------------------------
# Hungarian Method
# ------------------------------------------------------------------

class SolverHungarian(Solver):
    """
    Solver that uses the 'Hungarian' (Munkres) class
    to find a matching that minimizes the sum of |val1 - val2|.
    """

    def __init__(self, grid):
        super().__init__(grid)
    
    def run(self):
        """
        1. Split the grid into two sets: A (i+j even) and B (i+j odd)
        2. Construct the cost matrix cost_matrix (of size len(A) x len(B)).
           - cost_matrix[a, b] = |valA - valB| if (a, b) are 'adjacent' and color allowed
           - or a very large number otherwise.
        3. Call the Hungarian(cost_matrix) class to solve the problem.
        4. Retrieve the assignment row->col, reconstruct the pairs (cellA, cellB).
        5. Store the result in self.pairs (so that the __str__ method and the parent score() method can display it).
        """
        # Split the grid in two sets : A (i+j even) and B (i+j odd)
        A = []
        B = []
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if self.grid.is_forbidden(i, j):
                    continue
                if (i + j) % 2 == 0:
                    A.append((i, j))
                else:
                    B.append((i, j))

        nA = len(A)
        nB = len(B)

        # -- 2) Construct the cost matrix
        BIG_COST = 10**9
        cost_matrix = np.zeros((nA, nB), dtype=np.float64)

        for iA, cellA in enumerate(A):
            (rA, cA) = cellA
            valA = self.grid.value[rA][cA]
            for iB, cellB in enumerate(B):
                (rB, cB) = cellB
                valB = self.grid.value[rB][cB]
                if self._are_adjacent(cellA, cellB) and self._valid_colors(self.grid, cellA, cellB):
                    cost_matrix[iA, iB] = abs(valA - valB)
                else:
                    cost_matrix[iA, iB] = BIG_COST

        # -- 3) Using the Hungarian() class
        hungarian_solver = Hungarian(cost_matrix, is_profit_matrix=False)
        hungarian_solver.calculate()  
        
        # -- 4) Reconstruct the pair list.
        pairs = []
        for (rowA, colB) in hungarian_solver.get_results():
            if rowA < nA and colB < nB:
                cost_value = cost_matrix[rowA, colB]
                # If it's the BIG_COST, it means that the pair is not actually matched.
                if cost_value < BIG_COST:
                    cell_left = A[rowA]
                    cell_right = B[colB]
                    pairs.append((cell_left, cell_right))

        self.pairs = pairs

    # Insofar as we use an implementation of a GitHub Khan-Munkres algortihm, we can't use the all_pairs()
    # method of the Grid class. Therefore, both small methods below enable to represent the conditions of 
    # the problem again.

    def _are_adjacent(self, cellA, cellB):
        """
        Returns True if two cell are adjacent and False otherwise.
        """
        (iA, jA) = cellA
        (iB, jB) = cellB
        dist = abs(iA - iB) + abs(jA - jB)
        return dist == 1
    
    def _valid_colors(self, grid, cellA, cellB):
        """
        This method returns True if a matching between two pair is legal, 
        ie, it respects the color rules, and False otherwise.
        """
        (i1, j1) = cellA
        (i2, j2) = cellB
        c1 = grid.color[i1][j1]
        c2 = grid.color[i2][j2]

        allowed = {
            0: [0,1,2,3],  # white
            1: [0,1,2],    # red
            2: [0,1,2],    # blue
            3: [0,3],      # green
            4: [],         # black
        }

        if c2 in allowed[c1] and c1 in allowed[c2]:
            return True
        return False


