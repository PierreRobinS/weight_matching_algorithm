"""
This is the grid module. It contains the Grid class and its associated methods.
"""
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

class Grid():
    """
    A class representing the grid. 

    Attributes: 
    -----------
    n: int
        Number of lines in the grid
    m: int
        Number of columns in the grid
    color: list[list[int]]
        The color of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    value: list[list[int]]
        The value of each grid cell: value[i][j] is the value in the cell (i, j), i.e., in the i-th line and j-th column. 
        Note: lines are numbered 0..n-1 and columns are numbered 0..m-1.
    colors_list: list[char]
        The mapping between the value of self.color[i][j] and the corresponding color
    """
    

    def __init__(self, n, m, color=[], value=[]):
        """
        Initializes the grid.

        Parameters: 
        -----------
        n: int
            Number of lines in the grid
        m: int
            Number of columns in the grid
        color: list[list[int]]
            The grid cells colors. Default is empty (then the grid is created with each cell having color 0, i.e., white).
        value: list[list[int]]
            The grid cells values. Default is empty (then the grid is created with each cell having value 1).
        
        The object created has an attribute colors_list: list[char], which is the mapping between the value of self.color[i][j] and the corresponding color

        Other items:
        ------------
        self.mark : list[list[bool]]
            Allow to pin a cell as True or False to moove in the grid with a memory.
        """
        self.n = n
        self.m = m
        if not color:
            color = [[0 for j in range(m)] for i in range(n)]            
        self.color = color
        if not value:
            value = [[1 for j in range(m)] for i in range(n)]            
        self.value = value
        self.colors_list = ['w', 'r', 'b', 'g', 'k', 'A']
        self.coordinates = [[(i,j) for j in range(m)] for i in range(n)]
        self.mark = [[False for j in range(m)] for i in range(n)]

    def __str__(self): 
        """
        Prints the grid as text.
        """
        output = f"The grid is {self.n} x {self.m}. It has the following colors:\n"
        for i in range(self.n): 
            output += f"{[self.colors_list[self.color[i][j]] for j in range(self.m)]}\n"
        output += f"and the following values:\n"
        for i in range(self.n): 
            output += f"{self.value[i]}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the grid with number of rows and columns.
        """
        return f"<grid.Grid: n={self.n}, m={self.m}>"

    def plot(self): 
        """
        Plots a visual representation of the grid.
        """

        custom_colors = ['#00ff00', 'red', 'black', 'white', 'blue']
        custom_cmap = LinearSegmentedColormap.from_list("cmap_perso", custom_colors)

        plt.pcolor(self.color, cmap=custom_cmap)
        plt.show()

        # TODO

    def is_forbidden(self, i, j):
        """
        Returns True is the cell (i, j) is black and False otherwise
        """
        return self.color[i][j]==4 or self.color[i][j]==5
        
    def is_peace(self,i,j):
        """
        Returns True if the cell (i,j) is white and False otherwise
        """
        if self.color[i][j]==0:
            return True
        else:
            return False
        
    def cost(self, pair):
        """
        Returns the cost of a pair
 
        Parameters: 
        -----------
        pair: tuple[tuple[int]]
            A pair in the format ((i1, j1), (i2, j2))

        Output: 
        -----------
        cost: int
            the cost of the pair defined as the absolute value of the difference between their values
        """
        i1 = pair[0][0]
        j1 = pair[0][1]
        i2 = pair[1][0]
        j2 = pair[1][1]
        v1 = self.value[i1][j1]
        v2 = self.value[i2][j2]
        result = abs(v1-v2)
        return result
    
    def local_pairs_dr(self, i, j):
        """
        Returns a list of all pairs than we can build from a given cell and the right and lower cell 
        Outputs a list of tuples of tuples [(c1, c2), (c1', c2'), ...] where each cell c1 etc. is itself a tuple (i, j)
        NB : returns on
        """
        n = self.n
        m = self.m
        output = []
        if self.is_forbidden(i,j) == False:
                    if i!=n-1 and j!=m-1:
                        if self.color[i][j]==self.color[i][j+1] or (self.color[i][j]==0 and self.is_forbidden(i,j+1)==False) or self.color[i][j+1]==0:
                            output.append(((i,j),(i,j+1)))
                        if self.color[i][j]==self.color[i+1][j] or (self.color[i][j]==0 and self.is_forbidden(i+1,j)==False) or self.color[i+1][j]==0:
                            output.append(((i,j),(i+1,j)))
                    elif i==n-1 and j!=m-1:
                        if self.color[i][j]==self.color[i][j+1] or (self.color[i][j]==0 and self.is_forbidden(i,j+1)==False) or self.color[i][j+1]==0:
                            output.append(((i,j),(i,j+1)))
                    elif i!=n-1 and j==m-1:
                        if self.color[i][j]==self.color[i+1][j] or (self.color[i][j]==0 and self.is_forbidden(i+1,j)==False) or self.color[i+1][j]==0:
                            output.append(((i,j),(i+1,j)))
        return output

    def all_pairs(self):
        """
        Returns a list of all pairs of cells that can be taken together. 

        Outputs a list of tuples of tuples [(c1, c2), (c1', c2'), ...] where each cell c1 etc. is itself a tuple (i, j)
        """
        output = []
        n = self.n
        m = self.m
        for i in range(n):
            for j in range(m):
                #print("i : "  + str(i) + " and j : " + str(j))
                cell_pairs = self.local_pairs_dr(i,j)
                if cell_pairs != []:
                    for pair in cell_pairs:
                        output.append(pair)
        return output

    @classmethod
    def grid_from_file(cls, file_name, read_values=False): 
        """
        Creates a grid object from class Grid, initialized with the information from the file file_name.
        
        Parameters: 
        -----------
        file_name: str
            Name of the file to load. The file must be of the format: 
            - first line contains "n m" 
            - next n lines contain m integers that represent the colors of the corresponding cell
            - next n lines [optional] contain m integers that represent the values of the corresponding cell
        read_values: bool
            Indicates whether to read values after having read the colors. Requires that the file has 2n+1 lines

        Output: 
        -------
        grid: Grid
            The grid
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            color = [[] for i_line in range(n)]
            for i_line in range(n):
                line_color = list(map(int, file.readline().split()))
                if len(line_color) != m: 
                    raise Exception("Format incorrect")
                for j in range(m):
                    if line_color[j] not in range(5):
                        raise Exception("Invalid color")
                color[i_line] = line_color

            if read_values:
                value = [[] for i_line in range(n)]
                for i_line in range(n):
                    line_value = list(map(int, file.readline().split()))
                    if len(line_value) != m: 
                        raise Exception("Format incorrect")
                    print(line_value)
                    value[i_line] = line_value
            else:
                value = []

            grid = Grid(n, m, color, value)
        return grid
