import math
import heapq
from filecmp import cmp

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

class Retta(object):
    m = q = 0
    def __init__(self, p1, p2):
        self.x_verticale = None
        self.trovaEquazione(p1, p2)
    # altri Attributi =   m  &  q, float

    def trovaEquazione(self, p1, p2): #trova il coefficiente angolare   m   di una retta
        if p1.y == p2.y:
            self.q = p1.y
        elif p1.x == p2.x:
            self.x_verticale = p1.x
        else:
            self.m = float((p2.y - p1.y) / (p2.x - p1.x))
            self.q = float(p1.y - (p1.x * self.m))

    def calcolaY(self, x):
        if self.x_verticale != None:
            return False
        else:
            return float((self.m * x) + self.q)

    def calcolaX(self, y):
        if self.x_verticale != None:
            return self.x_verticale
        else:
            return float((y - self.q) / self.m )

class VerticeTr(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    nome = None #A, B, C    in Minuscolo
    rette = []

class Triangolo (object):
    vertici = []
    rette = {}
    def __init__(self, v1, v2, v3):
        self.vertici.append(v1)
        self.vertici.append(v2)
        self.vertici.append(v3)
        self.ordinaVertici()
        self.trovaRette()

    def ordinaVertici(self):
        i = 1
        while i <= 2:
            if self.vertici[0].y < self.vertici[i].y:
                (self.vertici[0], self.vertici[i]) = (self.vertici[i], self.vertici[0])
            elif self.vertici[0] == self.vertici[i]:
                if self.vertici[0].x > self.vertici[i].x:
                    (self.vertici[0], self.vertici[i]) = (self.vertici[i], self.vertici[0])
            i += 1
        if (self.vertici[1].x + self.vertici[1].y) > (self.vertici[2].x + self.vertici[2].y) :
            (self.vertici[1], self.vertici[2]) = (self.vertici[2], self.vertici[1])
        self.vertici[0].nome = "A"
        self.vertici[1].nome = "B"
        self.vertici[2].nome = "C"

    def trovaRette(self): #retta 1 per A e B, la assegno ad entrambi
        #A = AB, AC
        #B = AB, BC
        #C = AC, BC
        #sono 3 rette, che si ripetono

        #aggiunta AB - BA, AC - CA, BC-CB
        rettaAB = Retta(self.vertici[0], self.vertici[1])
        rettaAC = Retta(self.vertici[0], self.vertici[2])
        rettaBC = Retta(self.vertici[1], self.vertici[2])
        self.rette["AB"] = rettaAB
        self.rette["AC"] = rettaAC
        self.rette["BC"] = rettaBC
        #self.vertici[0].rette.append(rettaAB)
        #self.vertici[0].rette.append(rettaAC)
        #self.vertici[1].rette.append(rettaBC)
        #print(self.vertici[0].rette[0].m)
        #print(self.vertici[0].rette[1].m)
        #print(self.vertici[0].rette[2].m)
        #print(self.vertici[1].rette[0].m)

        #self.vertici[0].rette['B'] = Retta(self.vertici[0], self.vertici[1])
        #self.vertici[1].rette['A'] = self.vertici[0].rette[self.vertici[1].nome]
        #self.vertici[1].rette['AB'] = rettaAB
        #self.vertici[0].rette['C'] = Retta(self.vertici[0], self.vertici[2])
        #self.vertici[2].rette['A'] = self.vertici[0].rette[self.vertici[2].nome]
        #self.vertici[1].rette['C'] = Retta(self.vertici[1], self.vertici[2])
        #self.vertici[2].rette['B'] = self.vertici[1].rette[self.vertici[2].nome]

    def getVertici(self):
        return self.vertici

# funzione di calcolo distanza Euristica (istintiva)
def euristica(end, nodo):
    dist_elevata = math.pow(end.x - nodo.x, 2) + math.pow(end.y - nodo.y, 2)
    return round(math.sqrt(dist_elevata), 5)

##################################################################
#       MAIN
#################################################################

#rappresentazione piano cartesiano in una griglia
grafo = Grafo(5, 5) #griglia x * y, parte da 0 quindi il valore max è x-1

start = Nodo(4, 4) #punto iniziale
end = Nodo (0, 0) #punto di arrivo

v1 = VerticeTr(2,3)
v2 = VerticeTr(2,4)
v3 = VerticeTr(1,3)
tr = Triangolo(v1, v2, v3)

for n in tr.vertici:
    print("Punto  X:", n.x, "Y:", n.y)
print("Equazioni Triangolo 1\nAB: y=", tr.rette["AB"].m, "x + ", tr.rette["AB"].q)
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
costo_finora = {} #dict per salvare i costi e confrontare i vantaggi dei percorsi
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

