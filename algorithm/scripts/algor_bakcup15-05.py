import math
import heapq
from filecmp import cmp

##################################################################
#       Classi
#################################################################
class Grafo(object):
    # Corrisponde alla griglia del piano cartesiano, i nodi sono i Vertici
    # è l'oggetto griglia che contiene tutti i nodi e li gestisce
    def __init__(self, x, y):
        self._nodes = []
        self._indices = {} #dizionario, chiave-valore
        self._triangoli = []
        self._indices_triangoli = {}
        for righe in range(y):
            for colonne in range(x):
                self.add_node(Nodo(righe, colonne))

    def add_node(self, nodo):
        if nodo not in self._indices:
            self._nodes.append(nodo)
            self._indices[nodo] = len(self._nodes) - 1
        #return self.get_node(nodo)

    def add_triangolo(self, tr):
        if tr not in self._triangoli:
            self._triangoli.append(tr)
            self._indices_triangoli[tr] = len(self._nodes) - 1
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

    def get_triangoli(self):
        return self._triangoli[:]

    def get_index(self, nodo):
        return self._indices[nodo]

    def get_indexes(self):
        return self._indices[:]
    ###########################################
    # RIMOZIONE Ostacoli
    ####################
    node_to_delete = []

    def removeTriangoli(self):
        for tri in self._triangoli:
                # _1]A a sx di B
            # _2]A.x = B.x - > Niente su A
            # _3]A a dx di B
            if tri.vertici[0].x < tri.vertici[1].x: #inizio con A rispetto a B, 3 casi. Interazioni tra rette AB e AC
                self.condemnNodo_usingNodo(tri.vertici[0]) #condanno A
                rip_est = tri.vertici[1].x - tri.vertici[0].x
                if tri.vertici[2].x < tri.vertici[1].x: #SE C a sx di B
                    rip_est -= tri.vertici[1].x - tri.vertici[2].x
                cnt_rip_est = 1
                while cnt_rip_est <= rip_est: #da A.x+1 a B.x, in Orizzontale
                    x_current = tri.vertici[0].x + cnt_rip_est
                    y_max = tri.rette["AC"].calcolaY(x_current)
                    y_min = tri.rette["AB"].calcolaY(x_current)
                    y_current = math.floor(y_max)
                    dif_current = y_max - y_current
                    dif_max = y_max - y_min
                    if dif_current < dif_max:
                        self.condemnNodo(x_current, y_current)
                        rip_int = y_current - math.ceil(y_min)
                        if rip_int >= 1:
                            cnt_rip_int = 1
                            while cnt_rip_int <= rip_int: #da yAC(x_current) a yAB(x_current), in Verticale
                                self.condemnNodo(x_current, (y_current - cnt_rip_int))
                                cnt_rip_int += 1
                    cnt_rip_est += 1
                #arrivati a B, altri 3 casi
                    # _1.1]B a sx di C
                # _1.2]B.x = C.x -> Niente
                # _1.3]B a dx di C
                if tri.vertici[1].x < tri.vertici[2].x:
                    self.condemnNodo_usingNodo(tri.vertici[2])  # condanno C
                    rip_est = tri.vertici[2].x - tri.vertici[1].x - 1 #la colonna di B già l'ho tolta
                    if rip_est >= 1:
                        cnt_rip_est = 1
                        while cnt_rip_est <= rip_est: #da B.x+1 a C.x-1, in Orizzontale
                            x_current = tri.vertici[1].x + cnt_rip_est
                            y_max = tri.rette["AC"].calcolaY(x_current)
                            y_min = tri.rette["BC"].calcolaY(x_current)
                            y_current = math.floor(y_max)
                            dif_current = y_max - y_current
                            dif_max = y_max - y_min
                            if dif_current < dif_max:
                                self.condemnNodo(x_current, y_current)
                                rip_int = y_current - math.ceil(y_min)
                                if rip_int >= 1:
                                    cnt_rip_int = 1
                                    while cnt_rip_int <= rip_int: #in Verticale
                                        self.condemnNodo(x_current, (y_current - cnt_rip_int))
                                        cnt_rip_int += 1
                            cnt_rip_est += 1
                    # 1.3]_B a dx di C
                elif tri.vertici[1].x > tri.vertici[2].x:
                    self.condemnNodo_usingNodo(tri.vertici[1])  # condanno B
                    rip_est = tri.vertici[1].x - tri.vertici[2].x - 1  # la colonna di B già l'ho tolta
                    if rip_est >= 1:
                        cnt_rip_est = 1
                        while cnt_rip_est <= rip_est:  # da B.x-1 a C.x+1, in Orizzontale
                            x_current = tri.vertici[2].x + cnt_rip_est
                            y_max = tri.rette["BC"].calcolaY(x_current)
                            y_min = tri.rette["AB"].calcolaY(x_current)
                            y_current = math.floor(y_max)
                            dif_current = y_max - y_current
                            dif_max = y_max - y_min
                            if dif_current < dif_max:
                                self.condemnNodo(x_current, y_current)
                                rip_int = y_current - math.ceil(y_min)
                                if rip_int >= 1:
                                    cnt_rip_int = 1
                                    while cnt_rip_int <= rip_int:  # in Verticale
                                        self.condemnNodo(x_current, (y_current - cnt_rip_int))
                                        cnt_rip_int += 1
                            cnt_rip_est += 1
                # 2]_A.x = B.x
            elif tri.vertici[0].x == tri.vertici[1].x:
                # vado a B, solo UN caso
                # _B a sx di C
                self.condemnNodo_usingNodo(tri.vertici[2])  # condanno C
                rip_est = tri.vertici[2].x - tri.vertici[1].x
                cnt_rip_est = 0
                while cnt_rip_est < rip_est:  # da A.x a C.x-1, in Orizzontale
                    x_current = tri.vertici[1].x + cnt_rip_est
                    y_max = tri.rette["AC"].calcolaY(x_current)
                    y_min = tri.rette["BC"].calcolaY(x_current)
                    y_current = math.floor(y_max)
                    dif_current = y_max - y_current
                    dif_max = y_max - y_min
                    if dif_current < dif_max:
                        self.condemnNodo(x_current, y_current)
                        rip_int = y_current - math.ceil(y_min)
                        if rip_int >= 1:
                            cnt_rip_int = 1
                            while cnt_rip_int <= rip_int:  # da yAC(x_current) a yAB(x_current), in Verticale
                                self.condemnNodo(x_current, (y_current - cnt_rip_int))
                                cnt_rip_int += 1
                    cnt_rip_est += 1
                # _3]A a dx di B
            else:
                self.condemnNodo_usingNodo(tri.vertici[1])  # condanno B
                rip_est = tri.vertici[0].x - tri.vertici[1].x
                if tri.vertici[2].x < tri.vertici[0].x:  # SE C a sx di B
                    rip_est -= tri.vertici[2].x - tri.vertici[0].x
                cnt_rip_est = 1
                while cnt_rip_est <= rip_est:  # in Orizzontale
                    x_current = tri.vertici[1].x + cnt_rip_est
                    y_max = tri.rette["AB"].calcolaY(x_current)
                    y_min = tri.rette["BC"].calcolaY(x_current)
                    y_current = math.floor(y_max)
                    dif_current = y_max - y_current
                    dif_max = y_max - y_min
                    if dif_current < dif_max:
                        self.condemnNodo(x_current, y_current)
                        rip_int = y_current - math.ceil(y_min)
                        if rip_int >= 1:
                            cnt_rip_int = 1
                            while cnt_rip_int <= rip_int:  # da yAC(x_current) a yAB(x_current), in Verticale
                                self.condemnNodo(x_current, (y_current - cnt_rip_int))
                                cnt_rip_int += 1
                    cnt_rip_est += 1

                # arrivati a C, 3 casi
                    # _1.1]A a dx di C
                # _1.2]A.x = C.x -> Niente
                # _1.3]A a s x di C
                if tri.vertici[2].x < tri.vertici[0].x:
                    self.condemnNodo_usingNodo(tri.vertici[0])  # condanno A
                    rip_est = tri.vertici[0].x - tri.vertici[2].x - 1 #la colonna di B già l'ho tolta
                    if rip_est >= 1:
                        cnt_rip_est = 1
                        while cnt_rip_est <= rip_est: #da B.x+1 a C.x-1, in Orizzontale
                            x_current = tri.vertici[1].x + cnt_rip_est
                            y_max = tri.rette["AB"].calcolaY(x_current)
                            y_min = tri.rette["AC"].calcolaY(x_current)
                            y_current = math.floor(y_max)
                            dif_current = y_max - y_current
                            dif_max = y_max - y_min
                            if dif_current < dif_max:
                                self.condemnNodo(x_current, y_current)
                                rip_int = y_current - math.ceil(y_min)
                                if rip_int >= 1:
                                    cnt_rip_int = 1
                                    while cnt_rip_int <= rip_int: #in Verticale
                                        self.condemnNodo(x_current, (y_current - cnt_rip_int))
                                        cnt_rip_int += 1
                            cnt_rip_est += 1
                # _1.3]A a sx di C
                elif tri.vertici[2].x > tri.vertici[0].x:
                    self.condemnNodo_usingNodo(tri.vertici[2])
                    rip_est = tri.vertici[2].x - tri.vertici[0].x - 1
                    if rip_est >= 1:
                        cnt_rip_est = 1
                        while cnt_rip_est <= rip_est:  # da B.x-1 a C.x+1, in Orizzontale
                            x_current = tri.vertici[0].x + cnt_rip_est
                            y_max = tri.rette["AC"].calcolaY(x_current)
                            y_min = tri.rette["BC"].calcolaY(x_current)
                            y_current = math.floor(y_max)
                            dif_current = y_max - y_current
                            dif_max = y_max - y_min
                            if dif_current < dif_max:
                                self.condemnNodo(x_current, y_current)
                                rip_int = y_current - math.ceil(y_min)
                                if rip_int >= 1:
                                    cnt_rip_int = 1
                                    while cnt_rip_int <= rip_int:  # in Verticale
                                        self.condemnNodo(x_current, (y_current - cnt_rip_int))
                                        cnt_rip_int += 1
                            cnt_rip_est += 1
            #fine if, A rispetto a B
        #fine for
        self.removeNodiCondemned()
        print( "gatto")
    #fine def, removeTriangoli()


    def condemnNodo(self, x, y):
        nodeDying = self.findNodo(x, y)
        if nodeDying not in self.node_to_delete:
            self.node_to_delete.append(nodeDying)

    def condemnNodo_usingNodo(self, nodo):
        if nodo not in self.node_to_delete:
            self.node_to_delete.append(nodo)

    def findNodo(self, x, y):
        nodoTemp = Nodo(x, y)
        for next in self.get_nodes():
            if next == nodoTemp:
                return next

    def removeNodiCondemned(self):
        for nextKill in self.node_to_delete:
            if nextKill in self._indices: #non li cancella dalla lista dei nodi ma ne annulla solo i valori
                self._nodes[self.get_index(nextKill)].x = None
                self._nodes[self.get_index(nextKill)].y = None
        self.node_to_delete.clear()

class Nodo(object):
    # Contiente solamente le coordinate e la lista dei vicini che inizialmente è vuota e viene
    # riempita solo se il nodo è di interesse al percorso che si sta cercando
    # ridefinisce i 'compare' tra le sue istanze in modo da poterli confrontare
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

class Triangolo (object):
    def __init__(self, v1, v2, v3):
        self.vertici = []
        self.rette = {}
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
        #self.vertici[0].nome = "A"
        #self.vertici[1].nome = "B"
        #self.vertici[2].nome = "C"

    def trovaRette(self):
        #A = AB, AC
        #B = AB, BC
        #C = AC, BC
        #sono 3 rette, che si ripetono

        rettaAB = Retta(self.vertici[0], self.vertici[1])
        rettaAC = Retta(self.vertici[0], self.vertici[2])
        rettaBC = Retta(self.vertici[1], self.vertici[2])
        self.rette["AB"] = rettaAB
        self.rette["AC"] = rettaAC
        self.rette["BC"] = rettaBC

    def getVertici(self):
        return self.vertici

class VerticeTr(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.nome = None

class Retta(object):
    def __init__(self, p1, p2):
        self.m = self.q = 0
        self.x_verticale = None
        self.trovaEquazione(p1, p2)
    # altri Attributi =   m  &  q, float
    equazione = ""

    def trovaEquazione(self, p1, p2): #trova il coefficiente angolare   m   di una retta
        if p1.y == p2.y: #SE punti sulla stessa retta orizzontale
            self.q = p1.y
            self.equazione = "y = {}".format(self.q)
        elif p1.x == p2.x: #SE punti sulla stessa retta verticale
            self.x_verticale = p1.x

            self.equazione = "x = {}".format(self.x_verticale)
        else:
            self.m = float((p2.y - p1.y) / (p2.x - p1.x))
            self.q = float(p1.y - (p1.x * self.m))
            self.equazione = "y = {}x + {}".format(self.m, self.q)

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

##################################################################
#       Funzioni
#################################################################
def euristica(end, nodo): # funzione di calcolo distanza Euristica (istintiva)
    dist_elevata = math.pow(end.x - nodo.x, 2) + math.pow(end.y - nodo.y, 2)
    return round(math.sqrt(dist_elevata), 5)

##################################################################
#       MAIN
#################################################################
def main():
    #rappresentazione piano cartesiano in una griglia
    grafo = Grafo(11, 11) #griglia x * y, parte da 0 quindi il valore max è x-1

    start = Nodo(0, 0) #punto iniziale
    end = Nodo (10, 10) #punto di arrivo

    v1 = grafo.findNodo(1,5)
    v2 = grafo.findNodo(1,1)
    v3 = grafo.findNodo(9,1)
    tr = Triangolo(v1, v2, v3)

    #v1 = grafo.findNodo(0, 14)
    #v2 = grafo.findNodo(20, 14)
    #v3 = grafo.findNodo(0, 13)
    #tr2 = Triangolo(v1, v2, v3)
    grafo.add_triangolo(tr)
    #grafo.add_triangolo(tr2)

    ##################################################################
    #       Rimozione Ostacoli
    #################################################################
    grafo.removeTriangoli()

    # grafo.condemnNodo(4, 2) #condanni un nodo aggiungendolo alla lista dei condannati
    # grafo.removeNodiCondemned() #rimuovi tutti i condannati

    ##################################################################
    #       Algoritmo A*
    #################################################################

    for nodo in grafo.get_nodes():
        if nodo == start:
            start = nodo #assegnazione dei veri Nodi già esistenti in griglia,per non duplicarli
        if nodo == end:
            end = nodo

    frontier = [] #coda a priorità, prendo prima quello con priorità minore
    heapq.heappush(frontier, (0.0, 0, start)) #punto iniziale, priorità
    came_from = {} #dict per ricostruire ogni percorso
    costo_finora = {} #dict per salvare i costi e confrontare i vantaggi dei percorsi
    came_from[start] = None
    costo_finora[start] = 0
    cnt = 0  # usato per la doppia priorità in modo da evitare stati di uguaglianza nella coda

    while not len(frontier) == 0: #finchè la coda non è vuota
        current = heapq.heappop(frontier)[2] #prende l'elemento nella coda con priorità minore

        if current == end: #se arrivati al punto d'arrivo
            break
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

main()

    #######»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»»####

    #for next in grafo.get_nodes():
        #if next.x == 4:
            #if next.y == 4:
                #for adj in next.get_adjacents():
                    #print (adj.x, adj.y)
                #print("X=", next.x, "Y=", next.y, "-> adjacents =", len(next.get_adjacents()))