# A point in R^2
class Point:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

# Implements the line in an affine linear way - {p | p = (x,y) + b}
class Line:

    def __init__(self, p1 : Point, p2 : Point) -> None:
        self.slope = None 
        self.offset = None

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
    