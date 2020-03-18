from collections import defaultdict, deque
import math
from queue import PriorityQueue
import heapq
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker


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

        # Initialisierung des Koordinatensystem zum Zeigen der Straßenkarte
        self.koordinatensystem = Koordinatensystem()
        self.koordinatensystem.zeichneStraßenkarte(
            self.startpunkt,
            self.zielpunkt,
            liste_knoten=self.graph.knoten,
            liste_verbindungen=self.liste_verbindungen
        )

        # Kürzester Weg vom Start- zum Zielpunkt und dessen Kosten wird berechnet
        kürzester_weg, kosten_kürzester_weg = self.astar3(
            self.startpunkt, self.zielpunkt, self.graph)

        # der kürzeste Weg wird blau im Koordinatensystem dargestellt
        self.koordinatensystem.zeichnePfad(
            kürzester_weg, 'b-', "Kürzester Weg")

        # von der kürzesten Strecke ausgehend, werden diejenigen Strecken ausgewählt, die noch im Bereich der eingegebenen maximalen Verlängerung sind
        max_verlängerung = float(
            input("Maximale Verlängerung in Prozent: ")) / 100

        maximale_kosten = kosten_kürzester_weg + \
            kosten_kürzester_weg * max_verlängerung

        # Aussortierung der Knoten
        mögliche_knoten = self.graph.knoten
        for knoten in mögliche_knoten.copy():
            # Distanz Startpunkt --> aktueller Knoten
            d1 = self.berechneLänge(self.startpunkt, knoten)

            # Distanz Knoten --> Zielpunkt
            d2 = self.berechneLänge(knoten, self.zielpunkt)

            summe = d1 + d2
            if summe > maximale_kosten:
                # ist die Summe der beiden Längen größer als die maximalen Kosten
                # so wird der Knoten aus den möglichen Knoten entfernt, da er nicht mehr in Frage kommt
                mögliche_knoten.remove(knoten)


        alle_hyperkanten = self.macheHyperkanten(mögliche_knoten, self.graph)
        
        
        #self.koordinatensystem.show()
        
        graph_hyperkanten = Graph()
        for hyperkante in alle_hyperkanten:
            graph_hyperkanten.add_Kante(
                hyperkante[0], hyperkante[-1], self.berechneObAbbiegen(hyperkante))
        
        # hier Dijkstra verwenden
        optimalster_weg = self.dijkstra(self.startpunkt, self.zielpunkt, graph_hyperkanten)
        länge_optimalster_weg = self.berechneLängePfad(optimalster_weg)
        # TODO: label bei KoordinatenSystem Pfad zeichnen entfernen
        self.koordinatensystem.zeichnePfad(optimalster_weg, 'g-', None)

        print("Kürzeste Kosten: ", kosten_kürzester_weg)
        print("Maximale Kosten: ", maximale_kosten)
        print("Kosten optimalster Weg: ", länge_optimalster_weg)

        self.koordinatensystem.show()
        
        
        # Weg mit am wenigsten Abbiegen
        graph_wenigsten_abbiegen = Graph()
        
        # jetzt sind alle Knoten mögliche Knoten der Hyperkanten
        mögliche_knoten_wenigsten_abbiegen = self.graph.knoten
        hyperkanten_wenigsten_abbiegen = self.macheHyperkanten(mögliche_knoten_wenigsten_abbiegen, self.graph)
        for hyperkante in hyperkanten_wenigsten_abbiegen:
            graph_wenigsten_abbiegen.add_Kante(
                hyperkante[0], hyperkante[-1], self.berechneObAbbiegen(hyperkante)
            )
        weg_wenigsten_abbiegen = self.dijkstra(self.startpunkt, self.zielpunkt, graph_wenigsten_abbiegen)
        
        self.koordinatensystem.zeichnePfad(weg_wenigsten_abbiegen, 'r-', None)
        self.koordinatensystem.show()
        

        
    def macheHyperkanten(self, mögliche_knoten: list, graph):
        # neue Kanten werden mit den möglichen Knoten erstellt
        # die neuen Kanten sollen 3 Knoten miteinander verbinden, sog. Hyperkanten (statt 2 Knoten)
        alle_hyperkanten = []
        for knoten in mögliche_knoten:
            hyperkanten = []
            nachfolger1_items = graph[knoten]
            for nachfolger1_item in nachfolger1_items:
                nachfolger1, gewichtung1 = nachfolger1_item[0]

                nachfolger2_items = graph[nachfolger1]

                for nachfolger2_item in nachfolger2_items:
                    nachfolger2, gewichtung2 = nachfolger2_item[0]
                    
                    # wenn der Nachfolger des Nachfolgers nicht der Ausgangsknoten ist 
                    if nachfolger2 != knoten:
                        hyperkanten.append([
                            knoten, nachfolger1, nachfolger2
                        ])
            alle_hyperkanten.extend(hyperkanten)
        print(alle_hyperkanten)
        return alle_hyperkanten


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
                    priority = neue_kosten + \
                        self.heuristisch(nächster_knoten, ziel)
                    priorityQueue.put(nächster_knoten, priority)
                    gekommen_von[nächster_knoten] = aktueller_knoten

        return gekommen_von, kosten_bis_jetz

    def astar2(self, start, ziel, graph):
        geschlossenes_set = set()
        gekommen_von = {}

        gscore = {start: 0}
        fscore = {start: self.heuristisch(start, ziel)}

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
        # https://rosettacode.org/wiki/A*_search_algorithm#Python

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
                return pfad, F[ziel]  # Fertig!

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

    def berechneLängePfad(self, pfad: list):
            """ berechnet die Summe der Teilverbindungen des gegebenen Pfad
            """
            sum = 0
            for i in range(len(pfad)):
                if i > 0:
                    sum += self.berechneLänge(pfad[i-1], pfad[i])
            return sum
    
    def berechneObAbbiegen(self, hyperkante: list):
        """ Berechnung, ob man bei der gegebenen Hyperkante, die aus 3 Knoten besteht, abbiegen muss """
        kante1, kante2 = hyperkante[:2], hyperkante[1:]
        steigung1 = self.berechneSteigungKante(kante1)
        steigung2 = self.berechneSteigungKante(kante2)
        if steigung1 == steigung2:
            return 0
        else:
            return 1

    def berechneSteigungKante(self, kante: tuple):
        """berechnet die Steigung der eingegebenen Kante."""
        (x1, y1), (x2, y2) = kante
        # Differenz der y-Koordinaten des Start- und Zielpunktes der gegebenen Kante
        y_diff = y2 - y1

        # Differenz der x-Koordinaten des Start- und Zielpunktes der gegebenen Kante
        x_diff = x2 - x1
        try:
            steigung = y_diff / x_diff
        # falls keine Veränderung in x-Richtung vorliegt, wird der Steigung die 'Zahl' unendlich zugewiesen
        except ZeroDivisionError:
            steigung = math.inf

        return steigung

    def dijkstra(self, start, ziel, graph):
        assert start in graph.knoten
        distanz = {knoten: inf for knoten in graph.knoten}
        vorheriger = {knoten: None for knoten in graph.knoten}
        distanz[start] = 0
        q = graph.knoten.copy()
        nachbarn = {knoten: set() for knoten in graph.knoten}
        
        for  start, ende, kosten in graph.kanten:
            nachbarn[start].add((ende, kosten))
            
        while q:
            u = min(q, key=lambda knoten: distanz[knoten])
            q.remove(u)
            if distanz[u] == inf or u == ziel:
                break
                
            for v, kosten in nachbarn[u]:
                alt = distanz[u] + kosten
                if alt < distanz[v]:
                    distanz[v] = alt
                    vorheriger[v] = u
        
        s, u = deque(), ziel
        while vorheriger[u]:
            s.appendleft(u)
            u = vorheriger[u]
        s.appendleft(u)
        return s
        
        

inf = float('inf')

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
            knoten for knoten in self.adjazenzliste
        )

    @property
    def kanten(self):
        kanten = []
        for item in list(self.adjazenzliste.items()):
            anfang = item[0]
            nachfolge_graphen = item[1]
            for graph in nachfolge_graphen:
                nachfolger, kosten = list(graph.items())[0]
                kanten.append(
                    [anfang, nachfolger, kosten]
                )
        return kanten
            
            

    def __getitem__(self, key):
        """ gibt den Zielknoten und die Gewichtung zurück """
        print("KEy: ", key)
        return [list(n.items()) for n in self.adjazenzliste[key]]


class Koordinatensystem():
    def __init__(self):
        fig, ax = plt.subplots()
        loc = plticker.MultipleLocator(base=1.0)
        ax.xaxis.set_major_locator(loc)
        plt.ylabel("y-Achse")
        plt.xlabel("x-Achse")
        plt.grid(True)

    def zeichneStraßenkarte(self, startpunkt: tuple, zielpunkt: tuple, liste_knoten: list, liste_verbindungen):

        # die Kanten zwischen den einzelnen Knoten werden schwarz gezeichnet
        self.zeichneWeg(liste_verbindungen, 'k-', label=None)

        # Alle Straßenknoten (Kreuzungen) werden als schwarzer Punkt gezeichnet
        x_koords = [knoten[0] for knoten in liste_knoten]
        y_koords = [knoten[1] for knoten in liste_knoten]

        plt.plot(x_koords, y_koords, 'ko', label='Kreuzungen')

        # Startpunkt wird rot dargestellt
        plt.plot(*startpunkt, 'ro', label='Startpunkt')

        # Zielpunkt wird grün dargestellt
        plt.plot(*zielpunkt, 'go', label='Zielpunkt')

        # für die Legende im Koordinatensystem
        # kürzester Weg wird blau dargestellt werden
        plt.plot([], [], 'b-', label='kürzester Weg')

        # TODO die scheiße is orange!!!
        # optimalster Weg wird grün dargestellt werden
        plt.plot([], [], 'g-', label='optimalster Weg')

    def zeichneWeg(self, liste_verbindungen, farbe: str, label: str):
        """ Zeichnet die gegebene Liste der Verbindungen mit der gegebenen Farbe und Label auf dem Koordinatensystem
            Format der gegebenen Liste:
            [
                ((x1, y1), (x2, y2)),
                ((x2, y2), (x3, y3)),
                ...
            ]
        """
        for verbindung in liste_verbindungen:
            (x1, y1), (x2, y2) = verbindung
            plt.plot((x1, x2), (y1, y2), farbe)

        # x_koords = []
        # y_koords = []
        # for verbindung in liste_verbindungen:
        #     (x1, y1), (x2, y2) = verbindung
        #     x_koords.extend((x1, x2))
        #     y_koords.extend((y1, y2))

        # plt.plot(x_koords, y_koords)

    def zeichnePfad(self, pfad: list, farbe: str, label: str):
        """ Zeichnet einen gegebenen Pfad mit der gegebenen Farbe und Label auf dem Koordinatensystem
            Format des gegebenen Pfads: [(x1, y1), (x2, y2), (x3, y3), ...], 
            wobei der Punkt P1 mit P2 und P2 mit P3 etc. verbunden ist            
            Diese Methode konvertiert sozusagen die gegebene Liste zum Format für die Methode zeichneWeg() 
            (Format siehe Methode zeichneWeg() )
        """
        liste_verbindungen = []
        for i in range(len(pfad)):
            if i > 0:
                knoten1 = pfad[i-1]
                knoten2 = pfad[i]
                liste_verbindungen.append((knoten1, knoten2))

        self.zeichneWeg(liste_verbindungen, farbe, label)

    def show(self):
        """ Koordinatensystem wird sichtbar angezeigt """
        plt.legend(loc='upper left', frameon=True)
        plt.show()


if __name__ == '__main__':
    eingabe1 = """
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

    eingabe2 = """ 
    162
    (0,0)
    (9,0)
    (2,0) (4,1)
    (0,2) (1,4)
    (1,3) (2,3)
    (0,1) (1,2)
    (5,2) (5,3)
    (1,7) (0,5)
    (7,2) (7,3)
    (1,5) (2,7)
    (4,1) (5,1)
    (2,0) (3,0)
    (4,1) (3,0)
    (2,2) (3,2)
    (3,1) (1,0)
    (1,6) (0,4)
    (1,5) (2,5)
    (5,1) (6,1)
    (0,0) (0,1)
    (4,1) (4,0)
    (0,2) (0,1)
    (9,7) (9,6)
    (5,1) (4,0)
    (6,1) (7,1)
    (9,6) (8,5)
    (4,1) (3,1)
    (5,1) (5,0)
    (5,1) (5,2)
    (3,2) (2,1)
    (5,1) (6,2)
    (9,5) (8,4)
    (5,1) (7,2)
    (7,1) (5,0)
    (2,1) (4,2)
    (9,5) (9,4)
    (6,1) (7,2)
    (7,1) (6,0)
    (4,0) (5,0)
    (9,5) (8,3)
    (7,1) (7,0)
    (7,1) (7,2)
    (2,1) (3,1)
    (4,2) (3,1)
    (7,1) (8,2)
    (5,0) (6,0)
    (5,2) (3,1)
    (6,2) (7,2)
    (8,7) (6,6)
    (8,6) (7,5)
    (8,5) (7,4)
    (9,7) (7,6)
    (9,6) (7,5)
    (9,5) (7,4)
    (7,0) (8,2)
    (7,0) (8,0)
    (7,2) (8,2)
    (8,2) (9,2)
    (7,0) (8,1)
    (3,6) (2,5)
    (3,6) (3,7)
    (2,7) (2,6)
    (7,0) (9,1)
    (8,2) (8,1)
    (6,3) (7,5)
    (3,6) (5,7)
    (8,0) (9,1)
    (8,2) (9,1)
    (9,0) (9,1)
    (9,2) (9,1)
    (3,6) (4,7)
    (5,4) (7,5)
    (3,5) (2,4)
    (2,6) (3,7)
    (6,4) (7,5)
    (4,4) (4,5)
    (7,4) (7,5)
    (0,5) (0,4)
    (5,4) (4,5)
    (8,1) (9,1)
    (1,4) (3,5)
    (2,5) (4,6)
    (6,6) (6,5)
    (6,6) (5,5)
    (5,7) (4,6)
    (6,5) (7,6)
    (2,4) (4,5)
    (6,6) (4,5)
    (3,4) (4,5)
    (4,6) (4,5)
    (4,6) (6,7)
    (7,7) (5,6)
    (4,5) (5,6)
    (5,6) (6,7)
    (1,7) (0,6)
    (1,6) (2,7)
    (1,5) (3,6)
    (1,6) (0,5)
    (1,5) (2,6)
    (8,7) (9,7)
    (1,5) (0,4)
    (8,6) (9,6)
    (8,5) (9,5)
    (1,4) (1,5)
    (9,4) (8,3)
    (9,4) (9,3)
    (8,4) (6,3)
    (8,3) (9,3)
    (8,4) (7,3)
    (8,7) (7,7)
    (8,6) (7,6)
    (8,5) (7,5)
    (8,4) (7,4)
    (6,3) (7,3)
    (4,4) (5,4)
    (6,3) (6,4)
    (3,6) (2,6)
    (6,3) (5,3)
    (5,4) (4,3)
    (5,4) (6,4)
    (1,1) (1,2)
    (4,4) (3,3)
    (3,5) (2,5)
    (4,3) (6,4)
    (5,4) (3,3)
    (4,3) (5,3)
    (6,4) (5,3)
    (3,6) (4,6)
    (4,3) (3,3)
    (0,0) (1,1)
    (2,2) (1,1)
    (3,7) (4,7)
    (1,2) (3,3)
    (5,1) (6,3)
    (7,5) (6,5)
    (6,6) (7,6)
    (2,2) (4,3)
    (3,2) (1,1)
    (1,2) (2,3)
    (3,3) (2,3)
    (3,3) (3,4)
    (2,4) (2,3)
    (2,4) (3,4)
    (7,2) (8,4)
    (6,5) (5,5)
    (0,0) (1,0)
    (0,0) (1,2)
    (2,0) (1,0)
    (1,4) (0,4)
    (1,4) (2,4)
    (2,3) (3,4)
    (3,2) (5,3)
    (5,2) (6,3)
    (5,5) (4,5)
    (4,6) (5,6)
    (0,2) (0,3)
    (0,2) (2,3)
    (1,4) (0,3)
    (1,3) (2,4)
    (1,7) (2,7)
    (8,2) (8,3)
    (8,2) (9,3)
    (4,2) (5,3)
    (7,2) (6,3)
    (9,2) (9,3)
    """.split()

    b = Berechnungen(eingabe1)

    g = Graph()

    g.add_Kante(0, 1, 1)
    g.add_Kante(1, 3, 2)

    print(g[3])
