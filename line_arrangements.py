import numpy as np
import sympy as sp
import itertools
import matplotlib.pyplot as plt
from dcel import Vertex, HalfEdge, Face

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

class LineSegment:

    def __init__(self, p1 : Point, p2 : Point) -> None:
        self.p1 = p1
        self.p2 = p2
        # Returns an array [a, b, c] that represents the line in format ax + by + c = 0
        self.linear_format = self.compute_linear_format()
        self.desmos = self.desmos_format()
        self.infinite_line = Line(p1, p2)
    
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
    
    # Given a point (x, y), checks if the point is in the bounding box given by the line segment
    def in_bounding_box(self, point) -> bool:
        
        min_x, max_x = min(self.p1.x, self.p2.x), max(self.p1.x, self.p2.x)
        min_y, max_y = min(self.p1.y, self.p2.y), max(self.p1.y, self.p2.y)

        if min_x <= point[0] <= max_x and min_y <= point[1] <= max_y:
            return True
        else:
            return False

# Given a set of distinct points, implements the configuration given by taking every possible lines
class PointConfiguration:

    # Initialised by a list of Point objects
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
        self.bounding_box = self.find_bounding_box()

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
    def find_line_intersection(self, line1 : Line, line2 : Line):
        
        if not self.intersects(line1, line2):
            print("The lines do NOT intersect!")
            return None
        
        arrl1 = line1.linear_format
        arrl2 = line2.linear_format

        # arrl1_normalization_factor = 10 ** min(self.division_factor(arrl1[0]), self.division_factor(arrl1[1]))
        # arrl2_normalization_factor = 10 **min(self.division_factor(arrl2[0]), self.division_factor(arrl2[1]))

        M = np.array([[arrl1[0], arrl1[1]],
               [arrl2[0], arrl2[1]]])
        
        B = np.array([-1 * arrl1[2], -1 * arrl2[2]])

        return np.linalg.solve(M, B)
    
    #
    def line_lineSegment_intersects(self, line : Line, lineSegment : LineSegment) -> bool:

        if not self.intersects(line, lineSegment.infinite_line):
            return False
        
        intersection = self.find_line_intersection(line, lineSegment.infinite_line)

        return lineSegment.in_bounding_box(intersection)
    
    
    def intersection_points(self) -> set:

        line_pairs = list(itertools.combinations(self.lines, 2))
        intersection_points = set()


        for line_pair in line_pairs:

            if not self.intersects(line_pair[0], line_pair[1]):
                continue
            else:
                intersection_points.add(tuple(self.find_line_intersection(line_pair[0], line_pair[1])))

        print(f'Number of Intersection Points: {len(intersection_points)}')

        return intersection_points
    
    # Computes all intersections and picks the largest box that contains all intersections (with extra area)
    def find_bounding_box(self):

        points = list(self.intersection_points())

        if not points:
            return None  # Return None for an empty set of points

        # Initialise min and max values with the first point
        min_x, min_y = points[0]
        max_x, max_y = points[0]

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

    # Initialised the DCEL structure on the bounding box
    def dcel_initialise(self):
        
        # Initialisation of the DCEL
        vertices = []
        half_edges = []
        faces = []

        # Initialise the vertices, faces and half edges with the bounding box
        bounding_box = self.bounding_box

        # v1 = Vertex(bounding_box[0] - 1, bounding_box[1] - 1)  # Bottom Left
        # v2 = Vertex(bounding_box[0] - 1, bounding_box[3] + 1) # Top Left
        # v3 = Vertex(bounding_box[2] + 1, bounding_box[1] - 1)  # Bottom Right
        # v4 = Vertex(bounding_box[2] + 1, bounding_box[3] + 1)  # Top Right

        v1 = [bounding_box[0] - 1, bounding_box[3] + 1] # Top Left    
        v2 = [bounding_box[0] - 1, bounding_box[1] - 1]  # Bottom Left
        v3 = [bounding_box[2] + 1, bounding_box[1] - 1]  # Bottom Right
        v4 = [bounding_box[2] + 1, bounding_box[3] + 1]  # Top Right

        vertices_ccw = []

        vertices_ccw.append(v1)
        vertices_ccw.append(v2)
        vertices_ccw.append(v3)
        vertices_ccw.append(v4)

        # Create vertices
        for x, y in vertices_ccw:
            vertices.append(Vertex(x, y))

        # Create half-edges
        for _ in range(8):  # 8 half-edges for a box (4 edges, each with 2 half-edges)
            half_edges.append(HalfEdge())

        # Create faces (exterior and interior)
        faces.append(Face())  # Exterior face
        faces.append(Face())  # Interior face

        # Connect half-edges - in the initialisation, even indexed edges are interior of the box - odd indexed edges are the exterior of the box
        for i in range(4):
            # Set origin for each half-edge
            half_edges[i*2].origin = vertices[i]
            half_edges[i*2+1].origin = vertices[(i+1)%4]

            # Set twin half-edges
            half_edges[i*2].twin = half_edges[i*2+1]
            half_edges[i*2+1].twin = half_edges[i*2]

            # Set next and prev for counter-clockwise traversal
            half_edges[i*2].next = half_edges[(i*2+2)%8]
            half_edges[i*2].prev = half_edges[(i*2-2)%8]

            # Set next and prev for clockwise traversal
            half_edges[i*2+1].next = half_edges[(i*2-1)%8]
            half_edges[i*2+1].prev = half_edges[(i*2+3)%8]

            # Set incident face
            half_edges[i*2].incident_face = faces[1]  # Interior face
            half_edges[i*2+1].incident_face = faces[0]  # Exterior face

            # Set incident edge for vertices
            vertices[i].incident_edge = half_edges[i*2]

        # faces[0] is the exterior of the box
        # faces[1] is the interior of the box
        # Set outer component for faces
        faces[0].outer_component = half_edges[1]  # Any exterior half-edge
        faces[1].outer_component = half_edges[0]  # Any interior half-edge

        # Update the object properties
        self.vertices = vertices
        self.half_edges = half_edges
        self.faces = faces

        return None


    def dcel(self):

        # Initialise the DCEL on the bounding box
        # Interior face of the box: faces[1]
        # Exterior face of the box: faces[0]
        self.dcel_initialise()


    def visualise(self) -> None:

        for line in self.lines:
            plt.axline((line.p1.x, line.p1.y), (line.p2.x, line.p2.y))

        bounding_box = self.bounding_box

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

# points = [Point(0,1), Point(1,0), Point(-1,0), Point(0,-1), Point(0.6, 0.8)]
# PC = PointConfiguration(points)
# print(PC.line_arrangement.intersection_points())
# print(PC.line_arrangement.find_bounding_box())
# PC.line_arrangement.visualise()

hexagon = [Point(1,1), Point(1,-1), Point(-1, -1), Point(-1,1), Point(0.5,2), Point(-0.5,2), Point(0.5,-2), Point(-0.5,-2)]
hexagon_arrangement = PointConfiguration(hexagon)
LA = hexagon_arrangement.line_arrangement

LA.dcel()

print(len(LA.vertices))
print(len(LA.half_edges))
print(len(LA.faces))

print("-----")

for hedge in LA.half_edges:
    print([hedge.origin.x_coord, hedge.origin.y_coord])
    print([hedge.next.origin.x_coord, hedge.next.origin.y_coord])
    print("------------")

LA.visualise()


# LA = LineArrangement([])
# line = Line(Point(0,0), Point(1,1))
# lineSegment = LineSegment(Point(1,-1), Point(2,-2))
# 
# print(LA.line_lineSegment_intersects(line, lineSegment))
