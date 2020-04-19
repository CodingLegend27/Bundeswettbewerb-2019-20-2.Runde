#!/usr/bin/python

# 2. Runde Bundeswettbewerb Informatik 2019/20
# Autor: Christoph Waffler
# Aufgabe 3: Abbiegen

from collections import defaultdict, deque
import math
from queue import PriorityQueue
import heapq
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
import time
import sys
# Import von Tkinter
if sys.version_info.major == 2:
    import Tkinter as tk
    import Tkinter.scrolledtext as scrolledtext
    from Tkinter import messagebox
else:
    import tkinter as tk
    from tkinter import messagebox
    import tkinter.scrolledtext as scrolledtext


class Berechnungen:
    def __init__(self, eingabe: list, maximale_verlängerung: int, erweiterung_minAbbiegen: bool):
        # Zuweisung der Klassenvariablen durch die eingegebenen Daten
        self.erweiterung_minAbbiegen = erweiterung_minAbbiegen

        # Maximale Verlängerung wird festgelegt
        self.maximale_verlängerung = maximale_verlängerung

        # Anzahl der Straßen ist die erste Zahl der Eingabe
        self.anzahl_straßen = int(eingabe.pop(0))

        # Startpunkt ist die zweite Zahl
        self.startpunkt = self.zuPunkt(eingabe.pop(0))

        # Zielpunkt ist die dritte Zahl
        self.zielpunkt = self.zuPunkt(eingabe.pop(0))

        # alle Verbindungen zwischen zwei Kreuzungen hinzugefügt
        self.liste_verbindungen = [
            (self.zuPunkt(eingabe.pop(0)), self.zuPunkt(eingabe.pop(0)))
            for i in range(self.anzahl_straßen)
        ]

        # Aufruf der Hauptmethode
        self.main()

    def zuPunkt(self, eingabe: str):
        """ Methode zur Formatierung einer Zeile aus der eingabe mit Strings
        z.B.: '(14,0)' zu x=14, y=0


        Args:
            eingabe (str): String mit unformatierter Eingabe, Aufbau der Eingabe: '(x, y)'

        Returns:
            tuple. Ein Tuple mit den x- und y-Koordinaten der Kreuzung, die als int dargestellt sind.
        """

        # zuerst wird die Stelle des Kommas bestimmt
        ind_komma = eingabe.find(',')

        # die x-Koordinate wird durch die Ziffern bis zum Komma dargestellt
        x = int(eingabe[1: ind_komma])

        # die y-Koordinate wird durch die Ziffern vom Komma bis zum Ende dargestellt
        y = int(eingabe[ind_komma+1: -1])
        return (x, y)

    def main(self):
        """ Hauptmethode der Klasse und wird von __init__() aufgerufen """

        # Zeitmessung wird gestartet
        start_zeit = time.time()

        # ein Graph-Objekt wird erzeugt
        # dieser Graph besteht aus Kanten, welche wiederum aus zwei Knoten bestehen
        # die Länge einer Kante dient als Gewichtung
        self.graph = Graph()
        for kante in self.liste_verbindungen:
            strecke = self.berechneLänge(*kante)
            self.graph.add_Kante(*kante, strecke)

        # Initialisierung des Koordinatensystem zum Zeigen der Straßenkarte
        self.koordinatensystem = Koordinatensystem(self.erweiterung_minAbbiegen)
        self.koordinatensystem.zeichneStraßenkarte(
            self.startpunkt,
            self.zielpunkt,
            liste_knoten=self.graph.knoten,
            liste_verbindungen=self.liste_verbindungen
        )

        # Kürzester Weg vom Start- zum Zielpunkt und dessen Länge wird berechnet
        # A*-Algorithmus wird dabei verwendet
        kürzester_weg, länge_kürzester_weg = self.astar(self.startpunkt, self.zielpunkt, self.graph)
        anzahl_abbiegen_kürzester_weg = self.berechneAnzahlAbbiegenPfad(kürzester_weg)

        # der kürzeste Weg wird blau im Koordinatensystem dargestellt
        self.koordinatensystem.zeichnePfad(kürzester_weg, 'b-')

        # maximale Länge wird mithilfe der gegebenen maximalen Verlängerung (in %) berechnet
        maximale_länge = länge_kürzester_weg + \
            länge_kürzester_weg*(self.maximale_verlängerung/100)

        # optimaler Pfad wird ermittelt
        optimaler_pfad, länge_optimaler_pfad, anzahl_abbiegen_optimaler_pfad = self.optimalsterPfad(self.graph, self.startpunkt,
                                                                                                    self.zielpunkt, maximale_länge)
            
        umweg_optimaler_imVergleich_kürzester = länge_optimaler_pfad - länge_kürzester_weg



        if self.erweiterung_minAbbiegen:
            #### Erweiterung
            # Pfad mit minimalstem Abbiegen (ohne Eingrenzung) wird berechnet
            minAbbiegen_pfad, anzahl_abbiegen_minAbbiegen_pfad = self.minAbbiegenPfad(self.graph, self.startpunkt, self.zielpunkt)
            
            # Länge dieses Pfades
            länge_minAbbiegen_pfad = self.berechneLängePfad(minAbbiegen_pfad)
            
            # Umweg im Vergleich zum optimalen Pfad
            umweg_minAbbiegen_imVergleich_optimaler = länge_minAbbiegen_pfad - länge_optimaler_pfad
            
            # Umweg im Vergleich zum kürzesten Pfad
            umweg_minAbbiegen_imVergleich_kürzester = länge_minAbbiegen_pfad - länge_kürzester_weg
            
            # min Abbiegen-Pfad wird gezeichnet
            self.koordinatensystem.zeichnePfad(minAbbiegen_pfad, 'fuchsia')



        # optimaler Pfad wird gezeichnet am Schluss gezeichnet
        self.koordinatensystem.zeichnePfad(optimaler_pfad, 'y-')


        # Zeitmessung wird beendet
        ende_zeit = time.time()

        
        #### Konsolenausgaben        
        # Kürzester
        print(f"> Kürzester Weg: {kürzester_weg}")
        print(f" >> Länge kürzester Weg: {länge_kürzester_weg}")
        print(f" >> Anzahl Abbiegen kürzester Weg: {anzahl_abbiegen_kürzester_weg}")

        # Optimaler            
        print(f"\n> Optimaler Weg: {optimaler_pfad}")
        print(f" >> Länge optimaler Weg: {länge_optimaler_pfad}")
        print(f" >> Anzahl Abbiegen optimaler Weg: {anzahl_abbiegen_optimaler_pfad}")
        print(f" >>> Umweg im Vergleich zum kürzesten Weg: {umweg_optimaler_imVergleich_kürzester}; Maximal mögliche Länge war {maximale_länge}")

        if self.erweiterung_minAbbiegen:
            ### Erweiterung
            # Min Abbiegen
            print(f"\nErweiterung: Berechnung des Wegs mit geringster Anzahl an Abbiegevorgängen:")
            print(f"> 'min. Abbiegen Weg': {minAbbiegen_pfad}")
            print(f" >> Länge von 'min. Abbiegen Weg': {länge_minAbbiegen_pfad}")
            print(f" >> Anzahl Abbiegen: {anzahl_abbiegen_minAbbiegen_pfad}")
            print(f" >>> Umweg im Vergleich zum optimalsten Weg: {umweg_minAbbiegen_imVergleich_optimaler}")
            print(f" >>> Umweg im Vergleich zum kürzesten Weg: {umweg_minAbbiegen_imVergleich_kürzester}")
        
        # Zeitmessung wird ausgegeben
        print(f"\n>> Laufzeit des Programms: {ende_zeit-start_zeit} Sekunden \n (Start der Zeitmessung bei Aufruf der main-Methode)")

        self.koordinatensystem.show()


    def optimalsterPfad(self, graph, start: tuple, ziel: tuple, max_länge: int, pfad=[], bisher_optimalster_pfad=None, länge_bisherOptimalsterPfad=math.inf, anzahl_abbiegen_bisherOptimalsterPfad=math.inf):
        """ rekursive Methode zur Tiefensuche im gegebenen Graph
        
        Dabei wird die Tiefensuche abgebrochen, falls der aktuelle Pfad länger als maximal erlaubt ist.
        Ebenfalls wird die Tiefensuche abgebrochen, falls im aktuellen Pfad öfters abgebogen wird als der bisher optimalste Pfad (bisher beste)
        
        Args:
            graph (Graph): Datenstruktur Graph zum Verwalten der Straßen
            start (tuple): Startknoten 
            ziel (tuple): Zielknoten
            max_länge (int): maximale Länge des optimalen Pfads, wurde berechnet aus der maximalen Verlängerung (Eingabe des Benutzers)
            pfad (list): aktueller Pfad, zu dem der Startknoten hinzugefügt wird
            bisher_optimalster_pfad (list): zu Beginn 'None'. Falls der aktuelle Pfad den Zielknoten erreicht und nicht davor abgebrochen wird,
                                            gilt dieser Pfad als bisher optimalster Pfad.
            länge_bisherOptimalsterPfad (float): zu Beginn 'unendlich'. Wird ein bisher_optimalster_pfad gefunden, so wird die Länge dieses Pfades aktualisiert.
            anzahl_abbiegen_bisherOptimalsterPfad (float): zu Beginn 'unendlich'. Wird ein bisher_optimalster_pfad gefunden, so wird die Anzahl der Abbiegevorgänge dieses Pfades aktualisiert.
            
        Returns:
            list. der bisher_optimalster_pfad ist zum Schluss der Methode der beste optimalste Pfad und wird zurückgegeben
            float. Länge des besten optimalsten Pfades wird zurückgegeben
            float. Anzahl der Abbiegevorgänge des optimalesten Pfades wird zurückgegeben.        
        """
        # Startknoten wird zum aktuellen Pfad hinzugefügt
        pfad.append(start)

        # Länge des aktuellen Pfads wird berechnet
        länge_aktueller_pfad = self.berechneLängePfad(pfad)

        # Länge des aktuellen Pfads darf nicht länger als die maximale Länge sein
        if länge_aktueller_pfad <= max_länge:

            # die Anzahl der Abbiegevorgänge des aktuellen Pfads wird berechnet
            anzahl_abbiegen_aktueller_pfad = self.berechneAnzahlAbbiegenPfad(pfad)

            # die Anzahl der Abbiegevorgänge des aktuellen Pfads sollen weniger sein als beim bisher optimalsten Pfad
            if anzahl_abbiegen_aktueller_pfad <= anzahl_abbiegen_bisherOptimalsterPfad:
                
                # falls der aktuelle Knoten der Zielknoten ist
                if start == ziel:
                    
                    # Sonderfall: Anzahl Abbiegevorgänge des aktuellen und bisher optimalsten sind gleich,
                    # so wird der kürzere weiter verwendet
                    if anzahl_abbiegen_bisherOptimalsterPfad == anzahl_abbiegen_aktueller_pfad:

                        if länge_aktueller_pfad < länge_bisherOptimalsterPfad:
                            bisher_optimalster_pfad = pfad
                            länge_bisherOptimalsterPfad = länge_aktueller_pfad
                            anzahl_abbiegen_bisherOptimalsterPfad = anzahl_abbiegen_aktueller_pfad

                    # die Eigenschaften des bisher optimalsten Pfades werden aktualisiert, 
                    # da der aktuelle Pfad besser ist
                    else:
                        bisher_optimalster_pfad = pfad
                        länge_bisherOptimalsterPfad = länge_aktueller_pfad
                        anzahl_abbiegen_bisherOptimalsterPfad = anzahl_abbiegen_aktueller_pfad
                
                
                # Die Nachfolgeknoten werden anhand ihrem Abstand zum Zielknoten aufsteigend sortiert
                sortierte_liste_nachfolger = sorted(graph[start],
                                                    key=lambda item: self.berechneLänge(item[0][0], self.zielpunkt))
                                      
                for nachfolger_item in sortierte_liste_nachfolger:
                    
                    knoten, gewichtung = nachfolger_item[0]

                    # rekursiver Aufruf mit den Nachfolgerknoten
                    if knoten not in pfad:
                        bisher_optimalster_pfad, länge_bisherOptimalsterPfad, anzahl_abbiegen_bisherOptimalsterPfad = self.optimalsterPfad(graph, knoten, ziel, max_länge,
                                                                                                                                           pfad.copy(), bisher_optimalster_pfad, länge_bisherOptimalsterPfad, anzahl_abbiegen_bisherOptimalsterPfad)

        # der in diesem Teilgraphen optimalster Pfad wird zusammen mit seinen Eigenschaften zurückgegeben.
        return bisher_optimalster_pfad, länge_bisherOptimalsterPfad, anzahl_abbiegen_bisherOptimalsterPfad


    def heuristik_dfs(self, knoten: tuple, aktueller_pfad: list):
        """ Funktion zur Optimierung der Tiefensuche der Methode minAbbiegenPfad()
        
        Hierfür wird berechnet, wie oft man abbiegen müsste, falls der gegebene Knoten im aktuellen Pfad sein würde
        Diese Anzahl der Abbiegevorgänge im neuen Pfad wird zurückgegeben.
        
        Args:
            knoten (tuple): Knoten, der zu aktueller_pfad hinzugefügt wird
            aktueller_pfad (list): Ausgangspfad
            
        Returns:
            int. Anzahl der Abbiegevorgänge im neu entstandenen Pfad           
        
        """
        # Falls überhaupt bereits Knoten im aktuellen Pfad sind
        if aktueller_pfad:
            neuer_pfad = aktueller_pfad.copy()
            neuer_pfad.append(knoten)

            return self.berechneAnzahlAbbiegenPfad(neuer_pfad)
        
        # sind keine Knoten im aktuellen Pfad, so wird 0 zurückgegeben
        else:
            return 0

    def minAbbiegenPfad(self, graph, start: tuple, ziel: tuple, pfad=[], bisher_minAbbiegen_pfad=None, anzahl_abbiegen_bisherMinAbbiegen_pfad=math.inf):
        """ Methode zum Berechnen des Pfades mit minimalen Abbiegen ohne Eingrenzung
        
        Ziel dieser Methode ist es, denjenigen Pfad zu finden, in dem am wenigsten Mal abgebogen werden muss.
        Dabei wird der aktuelle Pfad verworfen, wenn man in diesem öfters abbiegen muss, als in dem bisher 'besten' Pfad (bisher_minAbbiegen_pfad).
        
        Args:
            graph (Graph): Datenstruktur Graph zum Verwalten der Straßen
            start (tuple): Startknoten 
            ziel (tuple): Zielknoten
            pfad (list): aktueller Pfad, zu dem der Startknoten hinzugefügt wird
            
            bisher_optimalster_pfad (list): zu Beginn 'None'. 
                Falls der aktuelle Pfad den Zielknoten erreicht und nicht davor abgebrochen wird, 
                gilt dieser Pfad als bisher optimalster Pfad.
                
            anzahl_abbiegen_bisherOptimalsterPfad (float): zu Beginn 'unendlich'. 
                Wird ein bisher_optimalster_pfad gefunden, so wird die Anzahl der Abbiegevorgänge dieses Pfades,
                also anzahl_abbiegen_bisherOptimalsterPfad, aktualisiert.
            
        Returns:
            list. der bisher_optimalster_pfad ist zum Schluss der Methode der beste optimalste Pfad und wird zurückgegeben
            float. Anzahl der Abbiegevorgänge des optimalesten Pfades wird zurückgegeben.        
        """
        
        # Aktueller Startknoten wird zum aktuellen Knoten hinzugefügt
        pfad.append(start)
        
        # Die Anzahl der Abbiegevorgänge im aktuellen Pfad werden berechnet
        anzahl_abbiegen_aktueller_pfad = self.berechneAnzahlAbbiegenPfad(pfad)
        
        # Falls diese Anzahl geringer als die Anzahl der Abbiegevorgänge des bisher 'besten' Pfades ist,
        # kann mit diesem aktuellen Pfad fortgefahren werden.
        if anzahl_abbiegen_aktueller_pfad < anzahl_abbiegen_bisherMinAbbiegen_pfad:
            
            # falls der aktuelle Knoten der Zielknoten ist
            if start == ziel:
                
                # aktueller Pfad ist nun der neue 'beste' Pfad mit geringster Anzahl an Abbiegevorgängen
                bisher_minAbbiegen_pfad = pfad
                anzahl_abbiegen_bisherMinAbbiegen_pfad = anzahl_abbiegen_aktueller_pfad
            
            # mithilfe der heuristischen Funktion heuristik_dfs wird für jedem Nachbarknoten ein Wert bestimmt
            # der beste Nachbarknoten ist derjenige, mit dem geringsten heuristischen Wert
            sortierte_liste_nachfolger = sorted(graph[start], 
                                                key=lambda item: self.heuristik_dfs(item[0][0], pfad))
            
            for nachfolger_item in sortierte_liste_nachfolger:
                nachfolger, gewichtung = nachfolger_item[0]

                
                if nachfolger not in pfad:

                    # die Methode wird rekursiv aufgerufen
                    bisher_minAbbiegen_pfad, anzahl_abbiegen_bisherMinAbbiegen_pfad = self.minAbbiegenPfad(graph, nachfolger,
                                                                                                            ziel, pfad.copy(), bisher_minAbbiegen_pfad, anzahl_abbiegen_bisherMinAbbiegen_pfad)
        
        return bisher_minAbbiegen_pfad, anzahl_abbiegen_bisherMinAbbiegen_pfad


    def astar(self, start, ziel, graph):
        """ A*-Algorithmus zur Berechnung des kürzesten Weg.
        
        Im gegebenen Graph soll vom Start- zum Zielknoten der kürzeste Weg berechnet werden.
        Dabei wird eine Schätzfunktion verwendet, um das Verfahren zu optimieren, indem der Abstand zum Zielknoten berechnet wird.
        Als Schätzfunktion wird die Methode heuristik_astar() verwendet, welche die Luftlinie berechnet.
            
        Args: 
            start (tuple): Startknoten
            ziel (tuple): Zielknoten
            graph (Graph): Graph als Datenstruktur
        
        Returns:
            list. Pfad mit dem Weg vom Start- zum Zielknoten
            float. Kosten für diesen Weg            
        """
        # Tatsächliche Kosten zu jedem Knoten vom Startknoten aus
        G = {}

        # Geschätzte Kosten vom Start zum Ende über die Knoten
        F = {}

        # Initialisierung der Startwerte
        G[start] = 0
        F[start] = self.heuristik_astar(start, ziel)

        # offene und geschlossene Knoten werden in einem Set gespeichert
        geschlossene_knoten = set()
        # zu Beginn wird der Startknoten zu den offenen Knoten hinzugefügt
        offene_knoten = set([start])
        # Verlauf des Wegs wir in gekommen_von gespeichert
        gekommen_von = {}

        # Solange noch ein Knoten offen ist:
        while len(offene_knoten) > 0:
            
            # Wähle den Knoten von der offenen Liste aus, der den geringsten F-Wert besitzen
            aktueller_knoten = None
            aktueller_F_wert = None

            for knoten in offene_knoten:
                if aktueller_knoten is None or F[knoten] < aktueller_F_wert:
                    aktueller_F_wert = F[knoten]
                    aktueller_knoten = knoten

            # Überprüfe, ob der Zielknoten erreicht wurde
            if aktueller_knoten == ziel:
                
                # falls ja, wird die Route rückwärts gegangen
                pfad = [aktueller_knoten]
                while aktueller_knoten in gekommen_von:
                    aktueller_knoten = gekommen_von[aktueller_knoten]
                    pfad.append(aktueller_knoten)
                
                # Pfad wird umgekehrt
                pfad.reverse()
                
                # der Pfad wird mit der Länge zurückgegeben
                return pfad, F[ziel]  # Fertig!

            # Markiere den aktuellen Knoten als geschlossen
            offene_knoten.remove(aktueller_knoten)
            geschlossene_knoten.add(aktueller_knoten)

            # Aktualisierung der Werte für die Nachbarknoten neben dem aktuellen Knoten
            for item in graph[aktueller_knoten]:
                nachbar_knoten, gewichtung = item[0]

                if nachbar_knoten in geschlossene_knoten:
                    # dieser Knoten wurde bereits ausgeschöpft
                    continue
                
                g_wert_kandidat = G[aktueller_knoten] + gewichtung

                # falls der Nachbarknoten noch nicht offen ist, 
                # wird er als offener gespeichert
                if nachbar_knoten not in offene_knoten:
                    offene_knoten.add(nachbar_knoten)
                
                elif g_wert_kandidat >= G[nachbar_knoten]:
                    # Wenn der G-Wert schlechter als der vorher gefundene ist
                    continue

                # G-Wert wird angepasst
                gekommen_von[nachbar_knoten] = aktueller_knoten
                G[nachbar_knoten] = g_wert_kandidat
                
                # Abstand zum Zielknoten wird geschätzt
                H = self.heuristik_astar(nachbar_knoten, ziel)
                F[nachbar_knoten] = G[nachbar_knoten] + H
        
        # Falls kein Weg gefunden wurde wird None zurückgegeben
        return None

    def heuristik_astar(self, knoten1, knoten2):
        """ Methode als heuristische Funktion im A*-Algorithmus
        
        Es wird der euklidische Abstand (Luftlinie) zwischen den beiden gegebenen Knoten berechnet.
        
        Args:
            knoten1: Startpunkt
            knoten2: Zielpunkt
        
        Returns:
            float. euklidische Distanz zwischen Start- und Zielpunkt    
            
        """
        # Methode berechneLänge wird verwendet
        return self.berechneLänge(knoten1, knoten2)


    def berechneLänge(self, knoten1: tuple, knoten2: tuple):
        """ Methode zur euklidischen Distanz zwischen zwei Knoten
        
        Args:
            knoten1: Startpunkt
            knoten2: Zielpunkt
        
        Returns:
            float. euklidische Distanz zwischen Start- und Zielpunkt
        """
        # c² = a² + b² wird angewendet (Pythagoras)
        (x1, y1) = knoten1
        (x2, y2) = knoten2
        return math.sqrt(
            (x1 - x2)**2 + (y1 - y2)**2 )

    def berechneLängePfad(self, pfad: list):
        """ Methode zur Berechnung der Summe der Teilverbindungen des gegebenen Pfad
        
        Dabei wird die Methode berechneLänge für alle Teilverbindungen des gegebenen Pfads aufgerufen.
        
        Args:
            pfad (list): Pfad, dessen Länge berechnet werden soll.
            
        Returns:
            float. Länge des Pfads
        """
        
        sum = 0
        for i in range(len(pfad)):
            if i > 0:
                # Für den aktuellen Punkt und seinen Vorgängerpunkt wird der Abstand berechnet.
                sum += self.berechneLänge(pfad[i-1], pfad[i])
        return sum

    def berechneAnzahlAbbiegenPfad(self, pfad: list):
        """ Berechnung der Anzahl, wie häufig auf dem gegebenen Pfad (Liste von Punkten) abgebogen werden muss.
        
        Args:
            pfad (list): Pfad
            
        Returns:
            float. Anzahl der Abbiegevorgänge im gegebenen Pfad
        """
        
        # Liste mit allen Steigungen der gegebenen Strecken wird berechnet
        steigungen = []
        for i in range(len(pfad)):
            if i > 0:
                steigungen.append(
                    self.berechneSteigungKante((pfad[i-1], pfad[i]))
                )

        # Für jeden Änderung des Betrags der aktuellen Steigerung wird der Zähler um 1 erhöht
        
        # die Anzahl der Abbiegevorgänge beträgt zu Beginn 0
        anzahl_abbiegen = 0

        for i in range(len(steigungen)):
            
            # die Steigung der aktuellen Strecke wird zugewiesen
            aktuell = steigungen[i]
            
            # falls es eine Strecke vor der aktuellen Strecke gibt
            if i > 0:
                # die Steigung der Strecke vor der aktuellen Strecke wird zugewiesen
                zuvor = steigungen[i-1]
                
                # wenn die beiden zugewiesenen Steigungen unterschiedlich sind,
                # wird der Zähler erhöht
                if aktuell != zuvor:
                    anzahl_abbiegen += 1

        return anzahl_abbiegen

    def berechneSteigungKante(self, kante):
        """berechnet die Steigung der eingegebenen Kante."""
        
        """ Methode zur Berechnung der aktuellen Steigung in der gegebenen Kante
        
        Args:
            kante: Liste aus zwei Punkten (Knoten)
        
        Returns:
            float. Steigung der Strecke der beiden Punkte
        
        """
        
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


class Graph:
    """ Klasse Graph zum Verwalten von Knoten und Kanten mit ungerichteten Gewichtungen """

    def __init__(self):
        """ Ein leeres Dictionary zum Speichern des Graphen wird erstellt.        
            Der Graph wird in Form einer Adjazenzliste gespeichert.        
        """
        self.adjazenzliste = defaultdict(list)

    def add_Kante(self, knoten1: tuple, knoten2: tuple, gewichtung):
        """ Methode zum Hinzufügen einer Kante.
        Die Kante besteht aus dem gegebenen Start- und Endknoten mit der gegebenen Gewichtung.
        
        Für diese Aufgabe wird ein ungerichteter Graph benötigt,
        daher muss die Kante für beide Knoten jeweils einmal als Start- 
        und einmal als Zielknoten hinzugefügt werden.
        
        Args:
            knoten1 (tuple): erster Knoten
            knoten2 (tuple): zweiter Knoten
            gewichtung (float): Gewichtung der Kante     
        """
        
        self.adjazenzliste[knoten1].append({
            knoten2: gewichtung})
        self.adjazenzliste[knoten2].append({
            knoten1: gewichtung
        })

    @property
    def knoten(self):
        return set(
            knoten for knoten in self.adjazenzliste
        )

    def __getitem__(self, key):
        """ Zurückgeben der Nachfolgeknoten zusammen mit deren Gewichtungen
        Args:
            key (tuple): Startknoten
        
        Returns:
            list. Liste mit Nachfolgeknoten
        """
        return [list(n.items()) for n in self.adjazenzliste[key]]


class EingabeFenster(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # Hintergrund des Fensters wird auf helles Grün gesetzt
        self['bg'] = '#d7efd7'
        self.erstelleEingabeFenster()

    def erstelleEingabeFenster(self):
        """ Erstellung des Eingabefensters """
        # Label
        self.label = tk.Label(
            text="Geben Sie im ersten Feld die Straßenkarte \nund im zweiten Feld die maximale Verlängerung in Prozent ein")
        self.label.pack(side=tk.TOP)

        # Eingabefeld für das Straßennetz
        self.textfeld_straßenkarte = scrolledtext.ScrolledText(
            self, width=40, height=10)
        self.textfeld_straßenkarte.insert(
            tk.END, "1. Feld: Straßennetz im Format des BwInf bitte hier einfügen:")
        self.textfeld_straßenkarte.pack(side=tk.TOP, fill=tk.BOTH)
        # Hintergrund des Eingabefelds wird auf helles Rot gesetzt
        self.textfeld_straßenkarte['bg'] = '#fed8d8'

        # Eingabe der maximalen Verlängerung
        self.textfeld_maximaleVerlängerung = tk.Entry(self, width=40)
        self.textfeld_maximaleVerlängerung.insert(
            tk.END, "2. Feld: maximalen Verlängerung in Prozent")
        self.textfeld_maximaleVerlängerung.pack(side=tk.TOP)
        # Hintergrund des Eingabefelds wird ebenfalls auf helles Rot gesetzt
        self.textfeld_maximaleVerlängerung['bg'] = '#fed7c7'

        self.erweiterung = tk.IntVar()
        self.checkbox_erweiterung = tk.Checkbutton(text="Erweiterung: Weg mit min. Anzahl Abbiegen ohne Begrenzung", variable=self.erweiterung)
        self.checkbox_erweiterung.pack(side=tk.TOP)

        # Button zum Starten
        self.button_start = tk.Button(
            self,
            width=10,
            height=5,
            text="Starte Berechnungen",
            command=self.starte)
        self.button_start.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.button_start['bg'] = '#49A'        

    def starte(self):
        """ Start! """
        # die Eingabe des Nutzers wird aus dem Textfenster gelesen
        eingabe = self.textfeld_straßenkarte.get('1.0', 'end').split()
        maximale_verlängerung = int(self.textfeld_maximaleVerlängerung.get())
        
        erweiterung = True if self.erweiterung.get() == 1 else False        
        
        # Eingabefenster wird geschlossen
        self.destroy()

        # Ruft die Klasse berechnungen auf, welche den Pfad berechnet,
        # den der Roboter zurücklegen muss, damit alle Batterien leer sind
        b = Berechnungen(eingabe, maximale_verlängerung, erweiterung)


class Koordinatensystem():
    def __init__(self, erweiterung_minAbbiegen):
        self.erweiterung_minAbbiegen = erweiterung_minAbbiegen
        fig, ax = plt.subplots()
        # loc = plticker.MultipleLocator(base=1.0)
        # ax.xaxis.set_major_locator(loc)
        plt.ylabel("y-Achse")
        plt.xlabel("x-Achse")
        plt.grid(True)

    def zeichneStraßenkarte(self, startpunkt: tuple, zielpunkt: tuple, liste_knoten: list, liste_verbindungen):

        # die Kanten zwischen den einzelnen Knoten werden schwarz gezeichnet
        self.zeichneWeg(liste_verbindungen, 'k-')

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

        # optimalster Weg wird gelb dargestellt werden
        plt.plot([], [], 'y-', label='optimalster Weg')
        
        if self.erweiterung_minAbbiegen:
            # Erweiterung: min Abbiegen-Weg wird in pink dargestellt
            plt.plot([], [], 'fuchsia', label='min. Abbiegen Weg')

    def zeichneWeg(self, liste_verbindungen, farbe: str):
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

    def zeichnePfad(self, pfad: list, farbe: str):
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

        self.zeichneWeg(liste_verbindungen, farbe)

    def show(self):
        """ Koordinatensystem wird sichtbar angezeigt """
        # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax = plt.gca()       
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])        
        
        ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        
        plt.show()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Eingabefenster")
    EingabeFenster(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
