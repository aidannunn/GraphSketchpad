
# vertex class. holds data on a vertex
class Vertex:
    def __init__(self, pos):
        self.pos = pos # stores a rect object with the vertex's position
        self.neighbors = [] # list of the vertex's neighbors
        self.degree = 0
        self.visited = False 
        self.color = 0
        self.display_color = 0
        self.colors = ["blue", "red", "green", "purple", "white", "orange", "yellow", "grey", "pink"]

    def __getitem__(self, key):
        return self.pos[key]

    def set_degree(self):
        self.degree = len(self.neighbors)

    def get_degree(self):
        return len(self.neighbors)
    
    def add_loop(self):
        self.degree = self.degree + 2


# edge class. holds data for an edge
class Edge:
    def __init__(self, pos, start, end):
        self.pos = pos # stores the rect the edge belongs to
        self.start = start # stores the center location of the rect (vertex) the edge starts at
        self.end = end # stores the center location of the rect (vertex) the edge ends at
    
    def __getitem__(self, key):
        return self.pos[key]

# graph class. stores overall data for the program's graph
class Graph:
    def __init__(self):
        self.verticies = []  # list of vertex objects
        self.edges = []  # list of edge objects
        self.n = 0 # number of vertices
        self.m = 0 # number of edges
        self.k = 0 # number of components
        self.bipartite = False # bool that states whether the graph is bipartite

    # method run after every program loop that updates n, m, and k, as well as degree for each vertex 
    # and removes edges if they are missing a vertex
    def update_graph(self):
        # update n, m, and k
        self.calc_n()
        self.calc_m()
        self.calc_k()

        if len(self.verticies) > 0:
            self.bipartite = self.check_bipartite()
            self.reset_visited()
            self.reset_colors()

        # refresh vertex degrees
        for vertex in self.verticies:
            vertex.set_degree()
            # check if the vertex has a self loop
            for edge in self.edges:
                if edge.start == edge.end and edge.start == vertex.pos.center:
                    vertex.add_loop()
                    

        # remove edges if it's not connected to two vertexes
        # get all current vertex positions
        vertex_positions = []
        for vertex in self.verticies: 
            if vertex.pos.center not in vertex_positions:
                vertex_positions.append(vertex.pos.center)

        # get edges to remove
        edges_to_remove = []
        for edge in self.edges:
            if edge.start not in vertex_positions or edge.end not in vertex_positions: 
                edges_to_remove.append(edge)
        # remove edges
        for edge in edges_to_remove:
            self.edges.remove(edge)
    
    # returns n, the number of vertices
    def calc_n(self):
        self.n = len(self.verticies)

    # returns m, the number of edges
    def calc_m(self):
        self.m = len(self.edges)
    
    # calculates k using Depth First Search
    # iterates through the vertices marks them as visited
    # for each vertex, it uses DFS to mark all of its neighbors and the neighbors neighbors as visited
    # when back in the initial for loop, if an unvisited vertex is found, DFS is performed on that one, too, 
    # and the count of components is incremented
    def calc_k(self):
        count = 0
        for vertex in self.verticies:
            if vertex.visited is False:
                # Do DFS and mark as visited
                self.depth_first_search1(vertex)
                count = count + 1
        self.k = count
        self.reset_visited()

    # DFS algorithm used in calculating k
    def depth_first_search1(self, v):
        v.visited = True
        for vertex in v.neighbors:
            if vertex.visited is False:
                self.depth_first_search1(vertex)
    
    # check if the graph is bipartite
    def check_bipartite(self):
        for vertex in self.verticies:
            if vertex.visited is False:
                vertex.visited = True
                vertex.color = 0
                if self.depth_first_search2(vertex, vertex.color) is False:
                    return False
        return True


    # DFS algorithm used in calculating bipartism
    def depth_first_search2(self, v, color):
        for vertex in v.neighbors:
            if vertex.visited is False:
                vertex.visited = True
                vertex.color = not color
                if (self.depth_first_search2(vertex, vertex.color) is False):
                    return False
            elif vertex.color == v.color:
                return False
        return True

    # reset visited vertexes to unvisited after calculating k
    def reset_visited(self):
        for vertex in self.verticies:
            vertex.visited = False
    
    # reset colors after determining bipartism
    def reset_colors(self):
        for vertex in self.verticies:
            vertex.color = 0

    # adds a vertex to the backend after it is created in the frontend
    def add_vertex(self, position):
        self.verticies.append(Vertex(position))

    # removes a vertex from the backend
    def remove_vertex(self, position):
        v = 0
        for vertex in self.verticies:
            if vertex.pos.collidepoint(position[0], position[1]):
                v = vertex
                break
        if len(self.verticies) > 0 and v is not 0:
            self.verticies.remove(v)
        
        # remove neighbors
        for neighbor in v.neighbors:
            neighbor.neighbors.remove(v)

        

    # adds an edge to the backend after it is created in the frontend
    def add_edge(self, rect, start, end):
        # add edge
        self.edges.append(Edge(rect, start, end))
        if start != end:
        # make two vertexes neighbors
            for vertex1 in self.verticies:
                if vertex1.pos.center == start:
                    for vertex2 in self.verticies:
                        if vertex2.pos.center == end:
                            vertex1.neighbors.append(vertex2)
                            vertex2.neighbors.append(vertex1)
                            break

    # removes an edge from the backend
    def remove_edge(self, position):
        e = None
        for edge in self.edges:
            if edge.pos.collidepoint(position[0], position[1]):
                e = edge
                break
        if len(self.edges) > 0 and e is not None:
            self.edges.remove(e)

        # remove neighbors
        if e.start != e.end:
            for vertex1 in self.verticies:
                if vertex1.pos.center == e.start:
                    for vertex2 in self.verticies:
                        if vertex2.pos.center == e.end:
                            vertex1.neighbors.remove(vertex2)
                            vertex2.neighbors.remove(vertex1)
                            break
    
    # change the color of a vertex
    def cycle_color(self, position):
        v = 0
        for vertex in self.verticies:
            if vertex.pos.collidepoint(position[0], position[1]):
                v = vertex
                break
        if v.display_color < 8:
            v.display_color = v.display_color + 1
        else:
            v.display_color = 0