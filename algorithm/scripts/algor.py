import math
import heapq

##################################################################
#       Classe GRAFO
#################################################################
#Corrisponde alla griglia del piano cartesiano, i nodi sono i Vertici
#è l'oggetto griglia che contiene tutti i nodi e li gestisce
class Grafo(object):
    def __init__(self, x, y):
        self._nodes = []
        self._indices = {} #dizionario, chiave-valore
        for righe in range(y):
            for colonne in range(x):
                self.add_node(Nodo(righe, colonne))

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

    def get_node_by_index(self, i):
        return self._nodes[i]

    def get_index(self, nodo):
        return self._indices[nodo]

    def get_indexes(self):
        return self._indices[:]
    ###########################################
    # RIMOZIONE Ostacoli
    ####################
    node_to_delete = []

    def condemnNodo(self, x, y):
        self.nodeDying = Nodo(x, y)

        for next in grafo.get_nodes():
            if next == self.nodeDying:
                self.nodeDying = next

        if self.nodeDying not in self.node_to_delete:
            self.node_to_delete.append(self.nodeDying)

    def removeNodiCondemned(self):
        for nextKill in self.node_to_delete:
            grafo.__removeNode__(nextKill)
        self.node_to_delete.clear()

    def __removeNode__(self, nodo): #non li cancella dalla lista dei nodi ma ne annulla solo i valori
        if nodo in self._indices:
            self._nodes[self.get_index(nodo)].x = None
            self._nodes[self.get_index(nodo)].y = None

##################################################################
#       Classe NODO
#################################################################
#Contiente solamente le coordinate e la lista dei vicini che inizialmente è vuota e viene
#riempita solo se il nodo è di interesse al percorso che si sta cercando
#ridefinisce i 'compare' tra le sue istanze in modo da poterli confrontare
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





##################################################################
#       MAIN
#################################################################

#rappresentazione piano cartesiano in una griglia
grafo = Grafo(1000, 1000) #griglia x * y, parte da 0 quindi il valore max è x-1

start = Nodo(956, 874) #punto iniziale
end = Nodo (0, 0) #punto di arrivo

##################################################################
#       Algoritmo A*
#################################################################

for nodo in grafo.get_nodes():
    if nodo == start:
        start = nodo #assegnazione dei veri Nodi già esistenti in griglia,per non duplicarli
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
    cnt = 0 #usato per la doppia priorità in modo da evitare stati di uguaglianza nella coda
    grafo.find_adjacents(current) #cerca i vicini solo del punto estratto dalla coda, non di tutti
    for next in current.get_adjacents():
        new_cost = costo_finora[current] + 1 # costo movimenti = 1, per tutti
        if next not in costo_finora or new_cost < costo_finora[next]:
            costo_finora[next] = new_cost
            priority = new_cost + euristica(end, next)
            heapq.heappush(frontier, (priority, cnt, next))
            came_from[next] = current
        cnt += 1
#####################################################
#       fine algoritmo, ricreo il percorso
##########################################
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

##################################################################
#       Rimozione Ostacoli
#################################################################





#######»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»####
#grafo.condemnNodo(4, 2) #condanni un nodo aggiungendolo alla lista dei condannati
#grafo.removeNodiCondemned() #rimuovi tutti i condannati

print ( "gat")


#for next in grafo.get_nodes():
    #if next.x == 4:
        #if next.y == 4:
            #for adj in next.get_adjacents():
                #print (adj.x, adj.y)
            #print("X=", next.x, "Y=", next.y, "-> adjacents =", len(next.get_adjacents()))

