import itertools

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

        Items:
        ------
        self.mark = (list(list(list(int)))) ist a cube of booleans to
        """
        self.grid = grid
        self.pairs = list()
        self.mark = dict()

    def score(self, pair_list):
        """
        Computes the score of thea list of pairs
        If there is some cases that don't match with any others, then it adds the value associated
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

class SolverTotal(Solver):

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
            - Takes only the legal ones the reject the other
            - Sort all the legal list 
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
        self.pairs = all_legal_pair_lists[0]
        return all_legal_pair_lists[0]
    

class SolverGreedy(Solver):

    #def __init__(self, grid):

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

    def run_real(self):
        """
        A greedy algorithm to try to solve the posed problem.
        It has some difficulties to find the best solution, but its results are correct and it is very much faster than the total solver.

        It works as following:
        ----------------------
            - First, it chooses a cell.
            - If the cell is black, it goes to the next.
            - Else, if the cell admit pairs, it computes the best pair associated with compute_min_dr()
            - It computes again the best pair with the cell already involved in the former pair.
            # PROBLEM NOT YET SOLVED : both pairs for a given cell can have the same cost, then compute_min_dr() chooses one pair randomly.
                - If there is no second pair, it adds the first one to self.pairs()
                - If both pairs are the same, then there is a match. It adds it to self.pairs()
                # PROBLEM NOT YET SOLVED : if the second cell admit another pair with an equal cost with the former one,
                the code actually chooses the first pair, even if it is not the best option.
                - If not, it runs the algorithm again (recursivity) to find the best pair of the second cell.
            - When one of the two first cases appears, the algorithm marks the cells with the color 5 to do not loop indefinitely.
            (The last steps works bc it is not possible to create pair with a color that is not in the rules of the game.)

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
                                print((cell[0], cell[1]), self.grid)
                                self.grid.color[cell[0]][cell[1]] = 5
                            self.pairs.append(min_pair_1[0])
                        # If there is no second pair, it adds the first one to self.pairs()
                        else:
                            if min_pair_1[1] <= min_pair_2[1]:
                                for cell in min_pair_1[0]:
                                    self.grid.color[cell[0]][cell[1]] = 5
                                self.pairs.append(min_pair_1[0])
                            # When there is a match. (Problem : using the '<=' symbol)
                            else:
                                self.run_real()
                                # When there is not.
                    else:
                        self.grid.color[i][j] = 5




