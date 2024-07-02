import numpy as np
import sympy as sp
import random

# A point in R^2
class Point:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

# Implements the line using 3 points to define the line
class Line:

    def __init__(self, p1 : Point, p2 : Point) -> None:
        self.p1 = p1
        self.p2 = p2
        # Returns an array [a, b, c] that represents the line in format ax + by + c = 0
        self.linear_format = self.compute_linear_format()
    
    def compute_linear_format(self) -> float:
        equation_matrix = sp.Matrix( np.array([[self.p1.x, self.p1.y, 1], 
                                     [self.p2.x, self.p2.y, 1]]) )
        nullspace = equation_matrix.nullspace()

        # Convert all elements to Rational
        rationals = [sp.Rational(elem) for elem in nullspace[0]]

        # Find the LCM of all denominators
        denominators = [r.q for r in rationals]
        lcm_value = sp.lcm(denominators)

        # Scale each element
        solution = [int(coord * lcm_value) for coord in nullspace[0]]

        return solution
        

# Creates a regular polygon with n sides
class RegularPolygon:
    
    def __init__(self, n) -> None:
        pass

    # Returns a list of lines
    def all_pairs_lines(self):
        pass


# Implements the line arrangement structure and algorithms
class LineArrangement:

    def __init__(self, lines : list) -> None:
        self.lines = lines
        self.vertices = None
        self.half_edges = None
        self.faces = None
        self.bounding_box = None

    # Returns true if the lines intersect
    def intersects(self, line1 : Line, line2 : Line) -> bool:

        arrl1 = line1.linear_format
        arrl2 = line2.linear_format

        M = np.array([[arrl1[0], arrl1[1]],
               [arrl2[0], arrl2[1]]])
        
        if np.linalg.matrix_rank(M) == 2:
            return True
        else:
            return False

    # Returns the intersection point of two lines if it exists
    def line_intersection(self, line1 : Line, line2 : Line):
        
        if not self.intersects(line1, line2):
            print("The lines do NOT intersect!")
        
        arrl1 = l1.linear_format
        arrl2 = l2.linear_format

        M = np.array([[arrl1[0], arrl1[1]],
                       [arrl2[0], arrl2[1]]])
        B = np.array([-1 * arrl1[2], -1 * arrl2[2]])

        return np.linalg.solve(M, B)
    
    # Computes all intersections and picks the largest box that contains all intersections (with extra area)
    def find_bounding_box(self):
        pass

    # Updates the bounding box given a new line and updating the 
    def update_bounding_box(self, line : Line):
        pass

    # Creates the 
    def dcel(self):
        pass

# IMPORTANT - How to ensure no issues occur in arrangements where the line perfectly crosses through the vertices - do not want numerical errors!

