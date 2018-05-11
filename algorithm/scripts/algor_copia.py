import math
import heapq

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

# funzione di calcolo distanza Euristica (istintiva)
def euristica(end, nodo):
    dist_elevata = math.pow(end.x - nodo.x, 2) + math.pow(end.y - nodo.y, 2)
    return round(math.sqrt(dist_elevata), 5)

#MAIN
#rappresentazione piano cartesiano in una griglia
grafo = Grafo()
for x in range(5):
    for y in range(5):
        grafo.add_node(Nodo(x,y))

#aggiunta vicini per ogni nodo
for next in grafo.get_nodes():
    grafo.find_adjacents(next)

#for next in grafo.get_nodes():
    #if next.x == 4:
        #if next.y == 4:
            #for adj in next.get_adjacents():
                #print (adj.x, adj.y)
            #print("X=", next.x, "Y=", next.y, "-> adjacents =", len(next.get_adjacents()))

#Algoritmo A*
start = Nodo(0, 0) #punto iniziale
end = Nodo (4, 4) #punto di arrivo

for nodo in grafo.get_nodes():
    if nodo == start:
        start = nodo
    if nodo == end:
        end = nodo

frontier = [] #coda a priorità, preso prima quello con priorità minore
heapq.heappush(frontier, (0.0, 0, start)) #punto iniziale, priorità
came_from = {} #dict per ricostruire ogni percorso
costo_finora = {} #dict per salvare  i costi e confrontare i vantaggi dei percorsi
came_from[start] = None
costo_finora[start] = 0

while not len(frontier) == 0: #finchè la coda non è vuota
    current = heapq.heappop(frontier)[2] #prende l'elemento nella coda con priorità minore

    if current == end: #se arrivati al punto d'arrivo
        break
    cnt = 0
    for next in current.get_adjacents():
        new_cost = costo_finora[current] + 1 # costo movimenti = 1, per tutti
        if next not in costo_finora or new_cost < costo_finora[next]:
            costo_finora[next] = new_cost
            priority = new_cost + euristica(end, next)
            heapq.heappush(frontier, (priority, cnt, next))
            came_from[next] = current
        cnt += 1

#fine algoritmo, ricreo il percorso
nodo_corrente = end
path = []
while nodo_corrente != start:
    path.append(nodo_corrente)
    nodo_corrente = came_from[nodo_corrente]
path.reverse()
print("#FROM Start[", start.x, ',', start.y, "] | TO End[", end.x, ',', end.y, "]")
for next in path:
    print("X:", next.x, "Y:", next.y)
print("#Costo:", costo_finora[end])
