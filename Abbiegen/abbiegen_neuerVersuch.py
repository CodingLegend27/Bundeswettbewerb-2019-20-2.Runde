from collections import defaultdict
import math
from queue import PriorityQueue
import heapq


class Berechnungen:
    def __init__(self, eingabe: list):
        # Zuweisung der Klassenvariablen durch die eingegebenen Daten
        self.anzahl_straßen = int(eingabe.pop(0))
        self.startpunkt = self.zuPunkt(eingabe.pop(0))
        self.zielpunkt = self.zuPunkt(eingabe.pop(0))

        self.liste_verbindungen = []
        for verbindung in range(int(len(eingabe)/2)):
            p1 = self.zuPunkt(eingabe.pop(0))
            p2 = self.zuPunkt(eingabe.pop(0))
            kante = (p1, p2)
            self.liste_verbindungen.append(kante)

        self.main()

    def zuPunkt(self, eingabe: str):
        """ verwertet die Eingabe zu einem Objekt der Klasse Punkt aufgebaut ist
        z.B.: '(14,0)'
        --> gibt einen Punkt als Tuple zurück"""
        # zuerst wird die Stelle des Kommas bestimmt
        ind_komma = eingabe.find(',')

        # die x-Koordinate wird durch die Ziffern bis zum Komma dargestellt
        x = int(eingabe[1: ind_komma])

        # die y-Koordinate wird durch die Ziffern vom Komma bis zum Ende dargestellt
        y = int(eingabe[ind_komma+1: -1])
        return (x, y)

    def main(self):
        """ Hauptmethode der Klasse und wird von __init__() aufgerufen """

        # ein Graph-Objekt wird erzeugt
        # dieser Graph besteht aus Kanten, welche wiederum aus zwei Knoten bestehen
        # die Länge einer Kante dient als Gewichtung
        self.graph = Graph()
        for kante in self.liste_verbindungen:
            strecke = self.berechneLänge(*kante)
            self.graph.add_Kante(*kante, strecke)
        
        gekommen, kosten = self.astar3(self.startpunkt, self.zielpunkt, self.graph)
        print(gekommen, kosten)
        
        
    def astar(self, start, ziel, graph):
        # https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
        # https://www.redblobgames.com/pathfinding/a-star/implementation.html
        """ Implementierung des A*-Algorithmus """
        # Speicherung des finalen Pfades vom Start zum Ziel
        path = []
        # bereits besuchte Knoten
        besuchte = []
        # TODO
        priorityQueue = PriorityQueue()
        priorityQueue.put(start, 0)
        gekommen_von = {}
        kosten_bis_jetz = {}
        gekommen_von[start] = None
        kosten_bis_jetz[start] = 0
        
        while not priorityQueue.empty():
            aktueller_knoten = priorityQueue.get()
            
            if aktueller_knoten == ziel:
                break
        
            for nächsten_knoten_item in graph[aktueller_knoten]:
                nächster_knoten, kosten = nächsten_knoten_item
                neue_kosten = kosten_bis_jetz[aktueller_knoten] + kosten
                
                if nächster_knoten not in kosten_bis_jetz or neue_kosten < kosten_bis_jetz[nächster_knoten]:
                    kosten_bis_jetz[nächster_knoten] = neue_kosten
                    priority = neue_kosten + self.heuristisch(nächster_knoten, ziel)
                    priorityQueue.put(nächster_knoten, priority)
                    gekommen_von[nächster_knoten] = aktueller_knoten
                
        return gekommen_von, kosten_bis_jetz
        
    def astar2(self, start, ziel, graph):
        geschlossenes_set = set()
        gekommen_von = {}
        
        gscore = {start: 0}
        fscore = {start:self.heuristisch(start, ziel)}
        
        offener_haufen = []
        
        heapq.heappush(offener_haufen, (fscore[start], start))
        
        while offener_haufen:
            aktueller_knoten = heapq.heappop(offener_haufen)[1]
            
            if aktueller_knoten == ziel:
                data = []
                while aktueller_knoten in gekommen_von:
                    data.append(aktueller_knoten)
                    aktueller_knoten = gekommen_von[aktueller_knoten]
                
                return data

            geschlossenes_set.add(aktueller_knoten)
            
    def astar3(self, start, ziel, graph):
        #https://rosettacode.org/wiki/A*_search_algorithm#Python
        
        # Tatsächliche Kosten zu jedem Knoten vom Startknoten aus
        G = {}   
        
        # Geschätze Kosten vom Start zum Ende über die Knoten
        F = {}
        
        # Initialisierung der Startwerte
        G[start] = 0
        F[start] = self.heuristisch(start, ziel)
        
        geschlossene_knoten = set()
        offene_knoten = set([start])
        gekommen_von = {}
        
        while len(offene_knoten) > 0:
            # Wähle die Knoten von der offenen Liste aus, die den geringsten F-Wert besitzen
            aktueller_knoten = None
            aktueller_F_wert = None
            
            for knoten in offene_knoten:
                if aktueller_knoten is None or F[knoten] < aktueller_F_wert:
                    aktueller_F_wert = F[knoten]
                    aktueller_knoten = knoten
                    
            # Überprüfe, ob der Zielknoten erreicht wurde
            if aktueller_knoten == ziel:
                # die Route rückwärts gehen
                pfad = [aktueller_knoten] 
                while aktueller_knoten in gekommen_von:
                    aktueller_knoten = gekommen_von[aktueller_knoten] 
                    pfad.append(aktueller_knoten)
                pfad.reverse()
                return pfad, F[ziel] # Fertig!

            # Markiere den aktuellen Knoten als geschlossen
            offene_knoten.remove(aktueller_knoten) 
            geschlossene_knoten.add(aktueller_knoten)
            
            # Aktualisierung der Werte für die Knoten neben dem aktuellen Knoten

            for item in graph[aktueller_knoten]:
                nachbar_knoten, gewichtung = item[0]
                print(nachbar_knoten)
                if nachbar_knoten in geschlossene_knoten:
                    # dieser Knoten wurde bereits ausgeschöpft
                    continue 
                kandidatG = G[aktueller_knoten] + gewichtung
                
                if nachbar_knoten not in offene_knoten:
                    offene_knoten.add(nachbar_knoten)
                elif kandidatG >= G[nachbar_knoten]:
                    # This G-Wert ist schlechter als der vorher gefundene
                    continue
                
                # Passe den G-Wert an
                gekommen_von[nachbar_knoten] = aktueller_knoten
                G[nachbar_knoten] = kandidatG
                # Abstand zum Zielknoten wird geschätzt
                H = self.heuristisch(nachbar_knoten, ziel)
                F[nachbar_knoten] = G[nachbar_knoten] + H
        
        raise RuntimeError("A* hat keine Lösung gefunden")
                
                
                
                
                
        
            
            
    
    def heuristisch(self, knoten1, knoten2):
        """ Methode als heuristische Funktion im A*-Algorithmus
            TODO wird das verwendet? 
            TODO Es wird der euklidische Abstand (Luftlinie) zwischen den beiden gegebenen Knoten berechnet
        """
        # Methode berechne Länge wird verwendet
        return self.berechneLänge(knoten1, knoten2)
        

    def berechneLänge(self, knoten1: tuple, knoten2: tuple):
        # c² = a² + b² wird angewendet (Pythagoras)
        (x1, y1) = knoten1
        (x2, y2) = knoten2
        return math.sqrt(
            (x1 - x2)**2
            +
            (y1 - y2)**2
        )
    
class Graph:
    """ Klasse Graph zum Verwalten von Knoten und Kanten mit ungerichteten Gewichtungen """

    def __init__(self):
        """ erstellt ein leeres Dictionary zum Speichern des Graphen """
        self.adjazenzliste = defaultdict(list)

    def add_Kante(self, knoten1: tuple, knoten2: tuple, gewichtung):
        """ fügt eine neue Kante zum Dictionary mit der gegebenen Gewichtung
            ungerichteter Graph, daher muss die Kante für beide Knoten jeweils einmal als Start- 
            und einmal als Zielknoten hinzugefügt werden
        """
        self.adjazenzliste[knoten1].append({
            knoten2: gewichtung})
        self.adjazenzliste[knoten2].append({
            knoten1: gewichtung
        })
    
    @property
    def knoten(self):
        # TODO
        return set(
            
        )
    
    @property
    def kanten(self):
        # TODO
        pass
    
    def __getitem__(self, key):
        """ gibt den Zielknoten und die Gewichtung zurück """
        return [list(n.items()) for n in self.adjazenzliste[key]]



if __name__ == '__main__':
    eingabe = """
    14
    (0,0)
    (4,3)
    (0,0) (0,1)
    (0,1) (0,2)
    (0,2) (0,3)
    (0,1) (1,1)
    (0,2) (1,1)
    (0,2) (1,3)
    (0,3) (1,3)
    (1,1) (2,2)
    (1,3) (2,2)
    (1,3) (2,3)
    (2,2) (2,3)
    (2,2) (3,3)
    (2,3) (3,3)
    (3,3) (4,3)
    """.split()

    b = Berechnungen(eingabe)
    

   
    g = Graph()
    
    g.add_Kante(0, 1, 1)
    g.add_Kante(1, 3, 2)
    
    print(g[3])
   
