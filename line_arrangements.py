import numpy as np
import sympy as sp
import itertools
import matplotlib.pyplot as plt
import random

# NUMERICAL STABILITY OF MATRIX RANK / SOLUTIONS
# FIND BOUNDING BOX




# A point in R^2
class Point:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class DuplicatePointError(ValueError):

    def __init__(self) -> None:
        super().__init__(self.__str__())
    
    def __str__(self):
        return "Duplicate Point Found - This application does not support duplicate points."

# Implements the line using 3 points to define the line
class Line:

    def __init__(self, p1 : Point, p2 : Point) -> None:
        self.p1 = p1
        self.p2 = p2
        # Returns an array [a, b, c] that represents the line in format ax + by + c = 0
        self.linear_format = self.compute_linear_format()
        self.desmos = self.desmos_format()
    
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
    
    def desmos_format(self) -> str:
        desmos = f'f(x) = ({self.linear_format[0]}) / (-1 * {self.linear_format[1]}) * x + ({self.linear_format[2]}) / (-1 * {self.linear_format[1]})'
        return desmos
        
# Given a set of distinct points, implements the configuration given by taking every possible lines
class PointConfiguration:

    # Initialized by a list of Point objects
    def __init__(self, points) -> None:
        self.points = points
        self.lines = self.all_pairs_lines()
        self.line_arrangement : LineArrangement = LineArrangement(self.lines)

    def all_pairs_lines(self):

        pairs = list(itertools.combinations(self.points, 2))

        for pair in pairs:
            if pair[0].x == pair[1].x and pair[0].y == pair[1].y:
                raise DuplicatePointError()
            
        lines = [Line(pair[0], pair[1]) for pair in pairs]
        return lines

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

    def division_factor(self, number):

        number = abs(number)
        
        if number <= 1:
            return 1

        magnitude = 0

        while 10**magnitude < number:
            magnitude += 1
        
        return magnitude - 1

    # Returns true if the lines intersect
    # NUMERICAL STABILITY OF RANK - NORMALIZE THE COLUMNS
    def intersects(self, line1 : Line, line2 : Line) -> bool:

        arrl1 = line1.linear_format
        arrl2 = line2.linear_format

        arrl1_normalization_factor = 10 ** min(self.division_factor(arrl1[0]), self.division_factor(arrl1[1]))
        arrl2_normalization_factor = 10 **min(self.division_factor(arrl2[0]), self.division_factor(arrl2[1]))

        M = np.array([[arrl1[0] / arrl1_normalization_factor, arrl1[1] / arrl1_normalization_factor],
               [arrl2[0] / arrl2_normalization_factor, arrl2[1] / arrl2_normalization_factor]])
        
        if np.linalg.matrix_rank(M) == 2:
            return True
        else:
            return False

    # Returns the intersection point of two lines if it exists
    def line_intersection(self, line1 : Line, line2 : Line):
        
        if not self.intersects(line1, line2):
            print("The lines do NOT intersect!")
        
        arrl1 = line1.linear_format
        arrl2 = line2.linear_format

        # arrl1_normalization_factor = 10 ** min(self.division_factor(arrl1[0]), self.division_factor(arrl1[1]))
        # arrl2_normalization_factor = 10 **min(self.division_factor(arrl2[0]), self.division_factor(arrl2[1]))

        M = np.array([[arrl1[0], arrl1[1]],
               [arrl2[0], arrl2[1]]])
        
        B = np.array([-1 * arrl1[2], -1 * arrl2[2]])

        return np.linalg.solve(M, B)
    
    
    def intersection_points(self) -> set:

        line_pairs = list(itertools.combinations(self.lines, 2))
        intersection_points = set()


        for line_pair in line_pairs:

            if not self.intersects(line_pair[0], line_pair[1]):
                continue
            else:
                intersection_points.add(tuple(self.line_intersection(line_pair[0], line_pair[1])))

        print(f'Number of Intersection Points: {len(intersection_points)}')

        return intersection_points
    
    # Computes all intersections and picks the largest box that contains all intersections (with extra area)
    def find_bounding_box(self):

        points = list(self.intersection_points())

        if not points:
            return None  # Return None for an empty set of points

        # Initialize min and max values with the first point
        min_x, min_y = points[0]
        max_x, max_y = points[0]

        print(min_x)

        # Iterate through the rest of the points
        for x, y in points[1:]:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        # Return the bounding box as (min_x, min_y, max_x, max_y)
        return (min_x, min_y, max_x, max_y)

    # Updates the bounding box given a new line and updating the 
    def update_bounding_box(self, line : Line):
        pass

    # Creates the 
    def dcel(self):
        pass

    def visualise(self) -> None:

        for line in self.lines:
            plt.axline((line.p1.x, line.p1.y), (line.p2.x, line.p2.y))

        bounding_box = self.find_bounding_box()

        corners = [(bounding_box[0] - 1, bounding_box[1] - 1),  # Bottom Left
                    (bounding_box[0] - 1, bounding_box[3] + 1), # Top Left
                   (bounding_box[2] + 1, bounding_box[1] - 1),  # Bottom Right
                   (bounding_box[2] + 1, bounding_box[3] + 1)]  # Top Right
        
        print(corners)
        
        plt.plot( (corners[0][0], corners[1][0]), (corners[0][1], corners[1][1]), linestyle='solid', color='black')
        plt.plot( (corners[0][0], corners[2][0]), (corners[0][1], corners[2][1]), linestyle='solid', color='black')
        plt.plot( (corners[1][0], corners[3][0]), (corners[1][1], corners[3][1]), linestyle='solid', color='black')
        plt.plot( (corners[3][0], corners[2][0]), (corners[3][1], corners[2][1]), linestyle='solid', color='black')

        plt.xlim(bounding_box[0] - 2, bounding_box[2] + 2)
        plt.ylim(bounding_box[1] - 2, bounding_box[3] + 2)

        plt.show()

# IMPORTANT - How to ensure no issues occur in arrangements where the line perfectly crosses through the vertices - do not want numerical errors!


points = [Point(0,1), Point(1,0), Point(-1,0), Point(0,-1), Point(0.6, 0.8)]
PC = PointConfiguration(points)
print(PC.line_arrangement.intersection_points())
print(PC.line_arrangement.find_bounding_box())
PC.line_arrangement.visualise()

# points2 = [Point(0,1), Point(0.6, 0.8), Point(-1,0), Point(0,-1)]
# PC2 = PointConfiguration(points2)
# 
# print(PC2.line_arrangement.intersection_points())
# PC2.line_arrangement.visualise()
# 
# line1 = Line(Point(0.6, 0.8), Point(0,1))
# line2 = Line(Point(-1,0), Point(0,-1))
# 
# LA = LineArrangement([])
# 
# print(LA.line_intersection(line1, line2))