# Thıs file contains very simple implementations of the Vertex / HalfEdge / Face of the DCEL (doubly-connected edge list) data structure

# Instead of an outgoing edge, we store all of them
class Vertex:

    def __init__(self, x, y) -> None:
        self.x_coord = x
        self.y_coord = y
    
    def incident_outer_edges(self):
        pass

class HalfEdge:

    def __init__(self, v_origin : Vertex, v_target : Vertex) -> None:
        self.origin = v_origin
        self.target = v_target
          
        self.twin : HalfEdge = None
        self.face : Face = None

        # These HalfEdge objects are the half edges that share the same face as self
        self.next_half_edge : HalfEdge = None
        self.prev_half_edge : HalfEdge = None

# The face can be determined by only one edge - but we create the half_edge_list object to make it accessible any time
# The structure is made so that there are no unbounded faces - as we will work within a bounding box
class Face:
    
    def __init__(self) -> None:
        self.half_edge_list = []
        self.vertex_list = set()