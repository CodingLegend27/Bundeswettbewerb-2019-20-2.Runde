# 2. Runde Bundeswettbewerb Informatik 2019/20
# from PySide2.QtCore import Qt
# from PySide2.QtWidgets import *
from tkinter import *
import math
import matplotlib as mlp
import matplotlib.pyplot as plt
import collections
import numpy as np
import matplotlib.ticker as plticker
from collections import defaultdict


# class Punkt():
#     def __init__(self, x: int, y: int):
#         self.x = x
#         self.y = y
#         self = (x, y)

#     def __str__(self):
#         """Ausgabe der Koordinaten eines Punktes."""
#         return f"({self.x}/{self.y})"

#     def __iter__(self):
#         return iter(self.x, self.y)


# class Kante():
#     def __init__(self, startpunkt: Punkt, zielpunkt: Punkt):
#         self.startpunkt = startpunkt
#         self.zielpunkt = zielpunkt

#         # Länge/Distanz der Kante wird als Gewichtung gespeichert
#         self.gewichtung = berechneLänge(startpunkt, zielpunkt)

#         self = (startpunkt, zielpunkt)

#     def __iter__(self):
#         """ implementierung der __iter__ - Methode, damit die Objekte von Kante iterierbar sind"""
#         return iter((self.startpunkt, self.zielpunkt))

#     def __str__(self):
#         print("Hello \n\n")
#         return f"Startpunkt: {startpunkt}; Zielpunkt: {zielpunkt}\n"


class EingabeFenster(Frame):

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.erstelleEingabeFenster()

        # TODO für Test
        # self.starte()

    def erstelleEingabeFenster(self):
        # Scrollbar
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Eingabefeld
        self.textfeld = Text(self, width=40, height=10)
        self.textfeld.insert(END, "Eingabe bitte hier rein")
        self.textfeld.pack(side=TOP)

        # Konfiguration der Scrollbar und des Textfelds
        self.scrollbar.config(command=self)
        self.textfeld.config(yscrollcommand=self.scrollbar.set)

        # Button zum Starten
        self.button_start = Button(
            self,
            width=10,
            height=5,
            text="Starte Berechnungen",
            command=self.starte)
        self.button_start.pack(side=BOTTOM, fill=BOTH)

    def starte(self):
        # die Eingabe des Nutzers wird aus dem Textfenster gelesen
        eingabe = self.textfeld.get('1.0', 'end').rsplit()

        # Eingabefenster wird geschlossen
        self.destroy()

        # Objekt der Klasse Berechnungen wird erzeugt
        # --> Berechnungen mit der erhaltenen Eingabe werden durchgeführt

        # # Für Testzwecke
        # eingabe = """
        # 14
        # (0,0)
        # (4,3)
        # (0,0) (0,1)
        # (0,1) (0,2)
        # (0,2) (0,3)
        # (0,1) (1,1)
        # (0,2) (1,1)
        # (0,2) (1,3)
        # (0,3) (1,3)
        # (1,1) (2,2)
        # (1,3) (2,2)
        # (1,3) (2,3)
        # (2,2) (2,3)
        # (2,2) (3,3)
        # (2,3) (3,3)
        # (3,3) (4,3)
        # """.rsplit()
        # b = Berechnungen(eingabe)
        # ansonsten
        b = Berechnungen(eingabe)


class Berechnungen():
    def __init__(self, eingabe: list):
        # Zuweisung der Klassenvariablen durch die eingegebenen Daten
        self.anzahl_straßen = int(eingabe.pop(0))
        self.startpunkt = self.zuPunkt(eingabe.pop(0))
        self.zielpunkt = self.zuPunkt(eingabe.pop(0))

        self.liste_verbindungen = []
        for verbindung in range(int(len(eingabe)/2)):
            #p1 = self.zuPunkt(eingabe.pop(0))
            p1 = self.zuPunkt(eingabe.pop(0))
            p2 = self.zuPunkt(eingabe.pop(0))
            kante = (p1, p2)
            self.liste_verbindungen.append(kante)

        self.graph = Graph()

        for verbindung in self.liste_verbindungen:
            self.graph.addKante(verbindung)

        self.liste_punkte = self.graph.Knoten()
        self.dictionary = self.graph.Dictionary()

        self.zeichneStraßenkarte()

        print("hello")

        # zu dieser Liste werden alle Pfade hinzugefügt
        self.alle_pfade = self.berechneAllePfade(
            self.startpunkt, self.zielpunkt, self.graph.Dictionary(), [], [], [], [])

        ####
        # TODO Alternativen aufräumen
        #self.sucheAllePfade(self.graph.Dictionary(), self.startpunkt, self.zielpunkt, [])

        #self.allePfade(self.startpunkt, self.zielpunkt)

        #self.alle_pfade = self.find_pfaddeee(self.graph.Dictionary(), self.startpunkt, self.zielpunkt, 100)

        #self.alle_pfade = self.get_all_paths(self.graph.Dictionary(), self.startpunkt, self.zielpunkt)
        ######

        print(f"\n\n Alle möglichen Wege: ", self.alle_pfade)

        # die Pfade in self.alle_pfade werden zu Tuples konvertiert und sind somit hashable und als key für ein Dictionary möglich
        self.alle_pfade = [tuple(pfad) for pfad in self.alle_pfade]

        # zu dieser Liste werden die Länge und die Anzahl der Abbiegevorgänge jedes einzelnen Pfades gespeichert
        länge_anzahlAbbiegen_alle_pfade = []

        for verbindung in self.alle_pfade:
            länge_anzahlAbbiegen_alle_pfade.append(
                [
                    self.berechneLängePfad(verbindung),
                    self.berechneAnzahlAbbiegenPfad(verbindung)
                ]
            )

        zipObj = zip(self.alle_pfade, länge_anzahlAbbiegen_alle_pfade)

        eigenschaften_alle_pfade = dict(zipObj)

        print(eigenschaften_alle_pfade)

        print("\n", eigenschaften_alle_pfade.items())

        # eigenschaften_alle_pfade.items() liefert beispielsweise:
        # (
        #   (
        #       (0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 2), (2, 3), (3, 3), (4, 3)
        #   ),
        #       [8.414213562373096, 4]
        # )
        # das Tuple ist wie folgt aufgebaut: (pfad, [länge_pfad, anzahl_abbiegen])

        # die kürzeste Strecke wird gefunden, indem die kleinste Zahl des ersten Elements der Eigenschaften-Liste des Tuples ermittelt wird
        pfad_kürzesteStrecke = min(
            eigenschaften_alle_pfade.items(), key=lambda x: x[1][0])
        print("Pfad mit kürzester Strecke: ", pfad_kürzesteStrecke)

        länge_kürzeste_Strecke = pfad_kürzesteStrecke[1][0]
        print("Länge dieses Pfads: ", länge_kürzeste_Strecke)

        # von der kürzesten Strecke ausgehend, werden diejenigen Strecken ausgewählt, die noch im Bereich der eingegebenen maximalen Verlängerung sind
        max_verlängerung = float(
            input("Maximale Verlängerung in Prozent: ")) / 100

        # die Länge eines Weges mit maximaler Verlängerung wird mithilfe der eingegebenen maximalen Verlängerung berechnet
        maximale_länge = länge_kürzeste_Strecke * \
            max_verlängerung + länge_kürzeste_Strecke
        print(maximale_länge)

        # von dem Dictionary werden nun alle Pfade entfernt, deren Länge größer als die maximal zulässige Länge
        # Umsetzung: von dem Dictionary wird eine Kopie erstellt, durch dessen Items mithilfe einer for-Schleife iteriert wird
        for pfad in eigenschaften_alle_pfade.copy().items():
            # ist die Länge des Pfades länger als die maximale Länge, wird der Pfad entfernt
            if pfad[1][0] > maximale_länge:
                eigenschaften_alle_pfade.pop(pfad[0])

        print("Aktualisierte Pfade: ", eigenschaften_alle_pfade)

        # von dem aktualisiertem Dictionary wird nun derjenige Pfad ausgewählt, bei welchem man am wenigsten abbiegen muss
        # die kleinste Zahl des zweiten Elements der Eigenschaften-Liste des Tuples liefert hierfür Auskunft über die Anzahl der Abbiegevorgänge im jeweiligen Pfad
        # dieser Pfad ist somit der optimalste Weg für Bilal
        optimaler_pfad = min(
            eigenschaften_alle_pfade.items(), key=lambda x: x[1][1])
        print(f"\n >> Optimalster Weg: {optimaler_pfad}")

        # Berechnung, um wie viel Prozent der optimalste Weg länger ist als der kürzeste Weg (in Prozent):
        umweg = (optimaler_pfad[1][0] -
                 länge_kürzeste_Strecke)/länge_kürzeste_Strecke
        print(
            f" >> zufahrender Umweg auf optimalstem Weg (im Vergleich zur kürzesten Strecke): {umweg*100} Prozent")

    def zuPunkt(self, eingabe: str):
        """ verwertet die Eingabe zu einem Objekt der Klasse Punkt aufgebaut ist
        z.B.: '(14,0)'
        --> gibt einen Punkt als Tuple zurück"""
        # zuerst wird die Stelle des Kommas bestimmt
        ind_komma = eingabe.find(',')
        # die x-Koordinate wird durch die Ziffern bis zum Komma dargestellt
        x = int(eingabe[1: ind_komma])
        # die y-Koordinate wird durch die Ziffer vom Komma bis zum Ende dargestellt
        y = int(eingabe[ind_komma+1: -1])
        return (x, y)

    def zeichneStraßenkarte(self):
        # Zeichenfenster wird erstellt
        # TODO: Zeichenfenster
        e = ZeichenFenster(root, width=700, height=700)
        e.pack(side="top", fill="both", expand=True)
        e.zeichne(
            startpunkt=self.startpunkt,
            zielpunkt=self.zielpunkt,
            liste_punkte=self.liste_punkte,
            liste_verbindungen=self.liste_verbindungen,
        )

        # neu
        # eine neues Koordinatensystem wird erstellt, indem die Straßenkarte gezeichnet wird
        self.k = Koordinatensystem()
        self.k.zeichneStraßenkarte(
            startpunkt=self.startpunkt,
            zielpunkt=self.zielpunkt,
            liste_punkte=self.liste_punkte,
            liste_verbindungen=self.liste_verbindungen)

    def berechneSteigungKante(self, kante: tuple):
        """berechnet die Steigung der eingegebenen Kante."""
        # Differenz der y-Koordinaten des Start- und Zielpunktes der gegebenen Kante
        y_diff = kante[0][1] - kante[1][1]

        # Differenz der x-Koordinaten des Start- und Zielpunktes der gegebenen Kante
        x_diff = kante[0][0] - kante[1][0]
        try:
            steigung = y_diff / x_diff
        # falls keine Veränderung in x-Richtung vorliegt, wird der Steigung die 'Zahl' unendlich zugewiesen
        except ZeroDivisionError:
            steigung = math.inf

        return steigung

    def berechneAnzahlAbbiegenPfad(self, pfad: list):
        """ Berechnung der Anzahl, wie häufig auf dem gegebenen Pfad (Liste von Punkten = Parameter) abgebogen werden muss
        """
        # Liste mit allen Steigungen der gegebenen Strecken wird erstellt
        steigungen = []
        # dabei wird die Methode berechneSteigungKante(tuple) aufgerufen
        for i in range(len(pfad)):
            if i > 0:
                steigungen.append(
                    self.berechneSteigungKante((pfad[i-1], pfad[i]))
                )

        # die Anzahl der Abbiegevorgänge beträgt zu Beginn 0
        anzahl_abbiegen = 0
        # TODO kommentare
        for i in range(len(steigungen)):
            # die Steigung der akutellen Strecke wird zugewiesen
            aktuell = steigungen[i]
            # falls es Strecke vor der aktuellen Strecke gibt
            if i > 0:
                # die Steigung der Strecke vor der aktuellen Strecke wird zugewiesen
                zuvor = steigungen[i-1]
                # wenn die beiden zugewiesenen Steigungen unterschiedlich sind,
                # wird der Zähler erhöht
                if aktuell != zuvor:
                    anzahl_abbiegen += 1

        # while steigungen:
        #     aktuell = steigungen[-1]
        #     zuvor = next(aktuell, None)
        #     if aktuell != zuvor:
        #         anzahl_abbiegen +=1
        # Rückgabewert: die Anzahl der Abbiegevorgänge im gegebenen Pfad
        return anzahl_abbiegen

    def berechneLänge(self, p1: tuple, p2: tuple):
        # c² = a² + b² wird angewendet (Pythagoras)
        return math.sqrt(
            (p1[0] - p2[0])**2
            +
            (p1[1] - p2[1])**2
        )

    def berechneLängePfad(self, pfad: list):
        """ berechnet die Summe der Teilverbindungen des gegebenen Pfad
        """
        sum = 0
        for i in range(len(pfad)):
            if i > 0:
                sum += self.berechneLänge(pfad[i-1], pfad[i])
        return sum

    # def berechneEigenschaftenPfade(self):
    #     """ Berechnet für jeden Pfad die Länge und die Anzahl der Abbiegevorgänge und speichert diese in einem Dictionary
    #         --> der erste Wert ist die Länge des Pfads, der zweite Wert die Anzahl der Abbiegungen
    #     """
    #     anzahl_pfade = len(self.alle_pfade)
    #     eigenschaften_pfade = {self.alle_pfade}

    #     pass

    # Hier sind die Möglichkeiten
    # 1. ist die bisher beste

    def berechneAllePfade(self, startpunkt, zielpunkt, graph: dict, aktuellerPfad, besucht, fertig, allePfade):
        """ Berechnung aller Pfade im Graph self.graph vom gegebenen Startpunkt zum gegebenen Zielpunkt
            Es wird davon ausgegangen, dass vom Startpunkt aus der Zielpunkt mindestens über einen Pfad erreichbar ist, da sonst die Aufgabenstellung nicht viel Sinn machen würde
        """
        besucht.append(startpunkt)
        aktuellerPfad.append(startpunkt)

        # falls der Startpunkt und der Zielpunkt identisch sind,
        # werden alle Pfade zusammen mit dem akutellen Pfad ausgegeben
        if startpunkt == zielpunkt:
            # aktuellerPfad.append(zielpunkt)

            print("aktueller pfad fertig: ", aktuellerPfad)
            # self.k.zeichneWeg(aktuellerPfad, 'g-')

            # zur Liste werden alle Pfade hinzugefügt, die mit dem zielpunkt enden
            # hier wird immer eine Kopie des aktuellen Pfads erstellt, da sonst der Pfad nach Beenden der Methode verloren gehen würde (eigene Erfahrung)
            allePfade.append(aktuellerPfad.copy())

        else:
            if startpunkt in graph:
                nachfolger = graph[startpunkt]
                if zielpunkt in nachfolger:
                    self.berechneAllePfade(
                        zielpunkt, zielpunkt, graph, aktuellerPfad, besucht, fertig, allePfade)
                else:
                    for i in graph[startpunkt]:
                        if i not in besucht:
                            self.berechneAllePfade(
                                i, zielpunkt, graph, aktuellerPfad, besucht, fertig, allePfade)

        fertig.append(aktuellerPfad.pop())
        besucht.remove(startpunkt)

        if not aktuellerPfad:
            return allePfade

    def sucheAllePfade(self, graph: dict, start, ziel, pfad):
        pfad.append(start)
        if start == ziel:
            self.alle_pfade.append(pfad)
        else:
            if graph[start]:
                for nachfolger in graph[start]:
                    if nachfolger not in pfad:
                        self.sucheAllePfade(graph, nachfolger, ziel, pfad)

        # if ziel in pfad:
        #         self.alle_pfade.append(pfad)

    def allePfadeHelper(self, graph: dict, start, ziel, besucht, pfad):
        besucht[start] = True
        pfad.append(start)

        if start == ziel:
            self.alle_pfade.append(pfad)
            print(">> Neuer Pfad gefunden: ", pfad)

        else:
            # Rekursion
            if start in graph:
                for nachfolger in graph[start]:
                    if besucht[nachfolger] == False:
                        self.allePfadeHelper(
                            graph, nachfolger, ziel, besucht, pfad)

        pfad.pop()
        besucht[start] = False

    def allePfade(self, start, ziel):
        zipObj = zip(self.liste_punkte, [
                     False for i in range(len(self.liste_punkte))])

        besucht = dict(zipObj)
        pfad = []
        self.allePfadeHelper(self.graph.Dictionary(),
                             start, ziel, besucht, pfad)

    def find_pfaddeee(self, graph: dict, startknoten, zielknoten, max_tiefe):
        pfade_gefunden = []
        self.find_pfade_helper(
            graph, startknoten, zielknoten, 0, max_tiefe, [], pfade_gefunden)
        return pfade_gefunden

    def find_pfade_helper(self, graph: dict, aktueller_knoten, zielknoten, aktuelle_tiefe, max_tiefe, aktueller_pfad: list, gefundene_pfade: list):
        aktueller_pfad.append(aktueller_knoten)

        if aktuelle_tiefe > max_tiefe:
            return

        if aktueller_knoten == zielknoten:
            print(">> Neuer Pfad: ", aktueller_pfad)
            gefundene_pfade.append(aktueller_pfad.copy())

            aktueller_pfad.pop()
            return

        else:
            for nachfolger in graph[aktueller_knoten]:
                self.find_pfade_helper(
                    graph, nachfolger, zielknoten, aktuelle_tiefe + 1, max_tiefe, aktueller_pfad, gefundene_pfade)

    def get_all_paths(self, graph, startknoten, zielknoten):
        return self.dfs(graph, startknoten, zielknoten, [], [], [])

    def dfs(self, graph, aktueller_knoten, zielknoten, besucht, pfad, alle_pfade):
        besucht.append(aktueller_knoten)
        pfad.append(aktueller_knoten)

        if aktueller_knoten == zielknoten:
            alle_pfade.append(pfad)

        for nachfolger in graph[aktueller_knoten]:
            if nachfolger not in besucht:
                self.dfs(graph, nachfolger, zielknoten,
                         besucht, pfad, alle_pfade)

        pfad.pop()
        besucht.pop()

        if not pfad:
            return alle_pfade

# TODO Verfahren mit Breitensuche und Backtracking (Recherchieren!)


class Graph():
    def __init__(self):
        """initialisiert einen Graph."""
        self.__graph_dict = defaultdict(list)

    def Dictionary(self):
        """ gibt das Dictionary sortiert wieder """
        self.__graph_dict = {
            k: sorted(self.__graph_dict[k]) for k in sorted(self.__graph_dict)}

        print(self.__graph_dict)
        print(self.Knoten())
        return self.__graph_dict

    def Knoten(self):
        """gibt die Knoten des Graphen wieder."""

        # ich brauch nicht nur die Keys also Schlüssel, sondern auch was hinter den Schlüsseln steht
        knoten = []
        keys = list(self.__graph_dict.keys())
        for key in keys:
            knoten.extend(self.__graph_dict[key])
        keys = list(set(keys))
        return knoten

    def Kanten(self):
        """gibt die Kanten des Graphen wieder."""
        return self.__generiereKanten()

    def addKnoten(self, knoten: tuple):
        """fügt die eingebenen Punkt als Kante zum Graphen brauch ich"""
        if knoten not in self.__graph_dict:
            self.__graph_dict[knoten] = []

    def addKante(self, kante: tuple):
        """fügt die eingebene Kante zum Graph."""
        knoten1, knoten2 = kante
        # if knoten1 in self.__graph_dict:
        # bei dieser Aufgabe handelt es sich um ungerichtete Kanten,
        # also Kanten die man in beide Richtungen 'befahren' kann,
        # also wie normale Straßen (keine Einbahnstraßen)
        # --> so muss dies auch bei dem Dictionary beachtet werden
        # --> bei beiden Knoten wird jeweils auch der andere Knoten hinzugefügt
        self.__graph_dict[knoten1].append(knoten2)
        self.__graph_dict[knoten2].append(knoten1)

        # else:
        #     self.__graph_dict[knoten1] = [knoten2]

    def __generiereKanten(self):
        """eine statische Methode die zum Erstellen der Kanten des Graphs, die
        in einer Liste zurückgegeben werden."""
        kanten = []
        for knoten in self.__graph_dict:
            for nachbar in self.__graph_dict[knoten]:
                for nachbar in self.__graph_dict[knoten]:
                    if (nachbar, knoten) not in kanten:
                        kanten.append({knoten, nachbar})
        return kanten

    def __str__(self):

        res = "Knoten: "
        # Knoten werden zum String hinzugefügt
        for knoten in self.__graph_dict:
            res += str(knoten) + " "

        res += "\nKanten: "
        # Kanten werden zum String hinzugefügt
        for kante in self.__generiereKanten():
            res += str(kante) + " "
        return res


class ZeichenFenster(Canvas):

    def __init__(self, parent, *args, **kwargs):
        Canvas.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.farbe_startpunkt = "red"
        self.farbe_zielpunkt = "red"
        self.farbe_knoten = "blue"

        # Koordinaten werden um diesen Faktor erweitert, damit sie auf der Zeichenfläche sichtbar sind
        self.faktor = 100
        self.radius_normaler_kreis = 20
        self.radius_besonderer_kreis = 25

        self.farbe_besonderer_kreis = "green"
        self.farbe_normaler_kreis = "blue"

        self.linien_dicke = 10
        self.farbe_linien = "black"

    def zeichne(self, startpunkt: tuple, zielpunkt: tuple, liste_punkte: list, liste_verbindungen: list):
        # Startpunkt
        startpunkt = self.zeichne_besonderen_kreis(
            x=startpunkt[0], y=startpunkt[1])
        zielpunkt = self.zeichne_besonderen_kreis(
            x=zielpunkt[0], y=zielpunkt[0])

        for punkt in liste_punkte:
            self.zeichne_normalen_kreis(x=punkt[0], y=punkt[1])

        for kante in liste_verbindungen:
            self.zeichne_linie(kante[0], kante[1])

        # for verbindung in:
        #     self.zeichne_linie()
        # TODO: diese punkte in liste_verbindungen sind ja die Punkte
        # TODO: Verbindungen zwischen den einzelnen Punkten machen
        # TODO: Speicherung in einem Graph vllt

    def zeichne_normalen_kreis(self, x: int, y: int):
        x *= self.faktor
        y *= self.faktor
        id = self.create_oval(x-self.radius_normaler_kreis, y-self.radius_normaler_kreis, x +
                              self.radius_normaler_kreis, y+self.radius_normaler_kreis, fill=self.farbe_normaler_kreis)
        return id

    def zeichne_besonderen_kreis(self, x: int, y: int):
        x *= self.faktor
        y *= self.faktor
        id = self.create_oval(x-self.radius_besonderer_kreis,
                              y-self.radius_besonderer_kreis, x +
                              self.radius_besonderer_kreis, y+self.radius_besonderer_kreis, fill=self.farbe_besonderer_kreis)
        return id

    def zeichne_linie(self, p1: tuple, p2: tuple):
        x1 = p1[0] * self.faktor
        y1 = p1[1] * self.faktor
        x2 = p2[0] * self.faktor
        y2 = p2[1] * self.faktor
        id = self.create_line(
            x1, y1, x2, y2, width=self.linien_dicke, fill=self.farbe_linien)
        return id


class Koordinatensystem():
    def __init__(self):
        plt.ylabel("y-Achse")
        plt.xlabel("x-Achse")
        plt.grid(True)
        fig, ax = plt.subplots()
        loc = plticker.MultipleLocator(base=1.0)
        ax.xaxis.set_major_locator(loc)

    def zeichneStraßenkarte(self, startpunkt: tuple, zielpunkt: tuple, liste_punkte: list, liste_verbindungen: list):

        # der Weg wird mit einer schwarzen Linie gezeichnet
        self.zeichneWeg(liste_verbindungen, 'k-')

        # neu
        # Start- und Zielpunkt von der Liste aller Punkten entfernen
        # liste_punkte.
        # liste_punkte.remove(zielpunkt)
        # liste_punkte.append(Punkt(4,4))
        # liste_punkte.remove()

        x_koord_punkte = []
        y_koord_punkte = []
        for punkt in liste_punkte:
            x_koord_punkte.append(punkt[0])
            y_koord_punkte.append(punkt[1])
            print("Punkt ", punkt[0], punkt[1])
        plt.plot(x_koord_punkte, y_koord_punkte, 'ko', label='Kreuzungen')

        # Startpunkt wird rot dargestellt
        plt.plot(startpunkt[0], startpunkt[1], 'ro', label='Startpunkt')
        # Zielpunkt wird grün dargestellt
        plt.plot(zielpunkt[0], zielpunkt[1], 'go', label='Zielpunkt')

        plt.legend(loc='upper left', frameon=True)
        plt.show()

    def zeichneWeg(self, liste_verbindungen: list, farbe: str):
        k = 0
        for verbindung in liste_verbindungen:
            # x-Koordinaten des Start- und Zielpunktes der Verbindung
            plt.plot((verbindung[0][0], verbindung[1][0]),
                     # y-Koordinaten des Start- und Zielpunktes der Verbindung
                     (verbindung[0][1], verbindung[1][1]),
                     farbe)
            k += 1
        print("Anzahl : ", k)


if __name__ == "__main__":
    root = Tk()
    EingabeFenster(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


# class Berechnungen:


"""
class StartFenster(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        self.button = QPushButton("Drücken")
        self.button.setAutoFillBackground(True)
        
        self.button.setDefault(True)
        ##se

    class Zeichenfenster(QWidget):
        scene = None
        
        def __init__(self, breite, höhe):
            QWidget.__init__(self)
            self.resize(breite, höhe)
            self.view = View()
            self.text = QLabel("Karte mit allen Straßen und Kreuzungspunkte")
            self.text.setAutoFillBackground(True)
            
            layout = QVBoxLayout(self)
            layout.addWidget(self.text)
            layout.addWidget(self.view)
            self.setWindowTitle("Karte mit Weg")
   """
