# Thıs file contains very simple implementations of the Vertex / HalfEdge / Face of the DCEL (doubly-connected edge list) data structure

# Instead of an outgoing edge, we store all of them
class Vertex:

    def __init__(self, x, y) -> None:
        self.x_coord = x
        self.y_coord = y
        self.incident_edge = None
    
    def incident_outer_edges(self):
        pass

class HalfEdge:

    def __init__(self) -> None:
        self.origin = None
        self.twin : HalfEdge = None
        self.incident_face : Face = None
        self.next : HalfEdge = None

        # Not necessary (equal to self.next.origin)
        self.target = None
        # Not necessary (equal to self.twin.next)
        self.prev_half_edge : HalfEdge = None


# The face can be determined by only one edge - but we create the half_edge_list object to make it accessible any time
# The structure is made so that there are no unbounded faces - as we will work within a bounding box
class Face:
    
    def __init__(self) -> None:
        self.outer_component = None
        self.inner_component = None
        self.half_edge_list = []
        self.vertex_list = set()