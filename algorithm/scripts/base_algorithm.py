class Grafo(object):
    def __init__(self):
        self._nodes = []
        self._indices = {} #dizionario, chiave-valore

    def add_node(self, nodo):
        if nodo not in self._indices:
            self._nodes.append(nodo)
            self._indices[nodo] = len(self._nodes) - 1
        #return self.get_node(nodo)

    def find_adjacents(self, nodo):
        dirs = [[-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1]]
        for dir in dirs:
            neighbor = Nodo(nodo.x + dir[0], nodo.y + dir[1])
            for next in self.get_nodes():
                if neighbor == next:
                    self.add_edge(nodo, next)

    def add_edge(self, u, v):
        node_u = self.get_node(u)
        node_v = self.get_node(v)
        node_v.add_adjacent(node_u)
        node_u.add_adjacent(node_v)

    def get_nodes(self):
        return self._nodes[:]

    def get_node(self, u):
        return self._nodes[self._indices[u]]

    def get_index(self, nodo):
        return self._indices[nodo]

class Nodo(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._adjacent = []

    def add_adjacent(self, a):
        if a not in self._adjacent:
            self._adjacent.append(a)

    def get_adjacents(self):
        return self._adjacent[:]

    def __eq__(self, other):
        if (self.x == other.x):
            if (self.y == other.y):
                return True
        return False
        #return self.x == other.x and self.y == other.y
    def __ne__(self, x):
        return not (x == self)
    def __hash__(self):
        return self.x.__hash__() and self.y.__hash__()

#MAIN
#rappresentazione piano cartesiano in una griglia
grafo = Grafo()
for x in range(6):
    for y in range(5):
        grafo.add_node(Nodo(x,y))

#aggiunta vicini per ogni nodo
for next in grafo.get_nodes():
    grafo.find_adjacents(next)

for next in grafo.get_nodes():
    if next.x == 5:
        if next.y == 4:
            for adj in next.get_adjacents():
                print (adj.x, adj.y)
            print("X=", next.x, "Y=", next.y, "-> adjacents =", len(next.get_adjacents()))