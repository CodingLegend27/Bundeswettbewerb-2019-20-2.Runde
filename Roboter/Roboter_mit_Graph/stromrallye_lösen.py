# 2. Runde Bundeswettbewerb Informatik 2019/20
from collections import defaultdict
import copy
import numpy as np
import time


import sys
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk


# https://de.wikipedia.org/wiki/L%C3%A4ngster_Pfad
#

# <BAUM>
# machen :D
' #TODO# '


class Steuerung:
    def __init__(self, eingabe: list):
        print(eingabe)
        # Größe des quadratischen Spielfelds
        self.size = int(eingabe.pop(0))
        
        # Aufbau: (x, y, ladung)
        self.roboter = self.zuPunkt(eingabe.pop(0))
        
        self.anzahl_batterien = int(eingabe.pop(0))
            
        # Aufbau: [(x1, y1, ladung1), (x2, y2, ladung2), ...]
        self.batterien = [self.zuPunkt(eingabe.pop(0)) for i in range(self.anzahl_batterien)]
        

        self.main2()
    
    def zuPunkt(self, eingabe: str):
        """ verwertet die Eingabe aus ('x, y, ladung') aufgebaut ist
        z.B.: '(14, 0, 1)'
        --> gibt einen Punkt als Tuple mit x-, y-Koordinate und Ladung als int zurück"""
        # erste Stelle des Kommas wird bestimmt
        ind_komma_1 = eingabe.find(',', 0, -1)

        # die x-Koordinate wird durch die Ziffern bis zum ersten Komma dargestellt
        x = int(eingabe[0:ind_komma_1])

        ind_komma_2 = eingabe.find(',', ind_komma_1+1, -1)

        # die y-Koordinate wird durch die Ziffern vom ersten Komma bis zum zweiten Komma dargestellt
        y = int(eingabe[ind_komma_1 + 1: ind_komma_2])

        # die Ladung wird durch die Ziffern vom zweiten Komma bis zum Ende dargestellt
        ladung = int(eingabe[ind_komma_2 + 1: ])
        
        # Ein Tuple aus x, y und Ladung wird zurückgegeben
        return (x, y, ladung)
    
    def erreichbareBatterien(self, x: int, y: int, ladung: int, restliche_batterien: list):
        """ mithilfe der Manhattan-Distanz werden alle Batterien ermittelt,
            von dem gegebenen Standort aus erreichbar sind
            --> der Betrag der Manhattan-Distanz gibt hier in dieser Aufgabe Auskunft darüber,
                wie viel Ladung zwischen zwei Positionen (zur Ersatzbatterie) benötigt wird
        """
        # die gegebene Ladung ist der maximal mögliche Betrag der Manhattan-Distanz
        # daher werden alle Batterien herausgefiltert, dessen Manhattan-Distanz größer als die gegebene Ladung ist
        # und die Distanz größer als 0 ist, damit sie sich nicht selbst als erreichbare Batterie sieht
        if ladung >= 0:
            erreichbare_batterien = list(filter(
                lambda batterie_item: self.manhattanDistanz(
                    x, y, batterie_item[0], batterie_item[1]) <= ladung and self.manhattanDistanz(
                    x, y, batterie_item[0], batterie_item[1]) > 0, restliche_batterien
            ))
            return erreichbare_batterien
        else:
            return []

    def manhattanDistanz(self, x1, y1, x2, y2):
        """ berechnet die Manhattan-Distanz zweier Punkte P1(x1/y1) und P2(x2/y2) 
            auf einem Schachbrettmuster-artigen Spielfeld
            --> dabei wird die Summe der Beträge der Differenz der x- und y-Koordinaten berechnet,
                welche die Manhatten-Distanz wiederspiegelt
            #Quelle: https://de.wikipedia.org/wiki/Manhattan-Metrik
        """
        delta_x = abs(x1 - x2)
        delta_y = abs(y1 - y2)
        distanz = delta_x + delta_y
        return distanz

    def anzahlErreichbarerBatterien(self, x: int, y: int, ladung: int, restliche_batterien: list):
        """ berechnet mithilfe der Methode erreichbareBatterien() die Anzahl der erreichbaren Batterien
        """
        erreichbare_batterien = self.erreichbareBatterien(
            x, y, ladung, restliche_batterien)
        anzahl = len(erreichbare_batterien)
        return anzahl

    def main(self):
        # Aktuelle Parameter sind die Startwerte des Roboters
        x_akt, y_akt, ladung_akt = self.roboter

        # die restlichen Batterien sind alle Batterien, die zu Beginn gegeben wurden
        restliche_batterien = self.batterien

        # die erreichbaren Batterien werden ausgewählt
        erreichbare_batterien = self.erreichbareBatterien(
            x_akt, y_akt, ladung_akt, restliche_batterien
        )

        anzahl_nachfolgende_batterien = list(map(
            lambda batterie: self.anzahlErreichbarerBatterien(
                *batterie, restliche_batterien), erreichbare_batterien
        ))

        # # https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-13.php

        # dieses Dictionary enthält die jeweiligen erreichbaren Dictionary als Key (x, y, ladung)
        # und mit der Anzahl der von ihnen aus erreichbaren nächsten Batterien als Key
        # z.B. (5, 1, 3): 1 --> bedeutet, dass von der Batterie mit Koordinaten (5, 1) und Ladung=3 aus eine Batterie erreichbar ist
        erreichbare_batterien_mit_anzahl_nachfolger = dict(
            zip(erreichbare_batterien, anzahl_nachfolgende_batterien))

        # die erreichbare Batterie mit der höchsten Anzahl an nächsten Batterien wird ausgewählt
        nächste_batterie = max(erreichbare_batterien_mit_anzahl_nachfolger)

        # Roboter "geht" zur nächsten Batterie
        # verbrauchte Ladung auf dem Weg zur Batterie wird berechnet
        verbrauchte_ladung = self.manhattanDistanz(
            *self.roboter[0:2], *nächste_batterie[0:2])

        # die verbrauchte Ladung wird von der Bordbatterie des Roboters abgezogen
        self.roboter[2] -= verbrauchte_ladung

        # die Ersatzbatterie am Boden wird mit der aktuellen Ladung der Bordbatterie getauscht
        ehemalige_bordbatterie_ladung = self.roboter[2]

        # die Ersatzbatterie wird aus den restlichen Batterien entfernt und ist jetzt die Bordbatterie des Roboters
        restliche_batterien.remove(nächste_batterie)
        self.roboter = nächste_batterie

        # zu den restlichen Batterien wird die jetzt am Boden liegende Ladung hinzugefügt, die die Ladung der ehemaligen Bordbatterie hat
        restliche_batterien.append(self.roboter[2].insert(
            2, ehemalige_bordbatterie_ladung))

        # Breitensuche gutes Video https://www.youtube.com/watch?v=7RCp2jNwxjQ

        pass

    def main2(self):
        # erstellt Graphen, um fügt für jede Ersatzbatterie
        # die jeweils mit der eigenen Ladung erreichbaren Batterien als Nachfolgeknoten zum Graph,
        # wobei die Gewichtung der Ladungsverbrauch zur Batterie ist
        # der Graph soll gerichtet sein
        self.graph = Graph()

        for batterie in self.batterien:
            # von der aktuellen Batterie aus werden alle erreichbaren Batterien ermittelt
            restliche_batterien = self.batterien.copy()
            restliche_batterien.remove(batterie)
            erreichbare_batterien = self.erreichbareBatterien(
                *batterie, restliche_batterien)

            # die erreichbaren Batterien bilden zusammen mit der aktuellen Batterie eine Kante,
            # wobei die aktuelle Batterie der Startknoten der Kante und die erreichbare Batterie der Endknoten der Kante ist
            # die Gewichtung der Kante ist die verbrauchte Ladung von der aktuellen Batterie zur erreichbaren Batterie
            for erreichbare_batterie in erreichbare_batterien:
                # nur die x- und y-Koordinaten der Batterien werden benötigt, die Ladung nicht
                x_start, y_start = batterie[:2]
                x_ende, y_ende = erreichbare_batterie[:2]

                # verbrauchte Ladung ist die Manhattan-Distanz
                verbrauchte_ladung = self.manhattanDistanz(
                    x_start, y_start, x_ende, y_ende)
                self.graph.add_Kante((x_start, y_start),
                                     (x_ende, y_ende), verbrauchte_ladung)

        # dasselbe wird ebenfalls für den Roboter durchgeführt
        roboter_erreichbare_batterien = self.erreichbareBatterien(
            *self.roboter, self.batterien)
        for erreichbare_batterie in roboter_erreichbare_batterien:
            x_start, y_start = self.roboter[:2]
            x_ende, y_ende = erreichbare_batterie[:2]
            verbrauchte_ladung = self.manhattanDistanz(
                x_start, y_start, x_ende, y_ende)
            self.graph.add_Kante((x_start, y_start),
                                 (x_ende, y_ende), verbrauchte_ladung)

        aktuelle_ladung_batterien = defaultdict(list)
        for batterie in self.batterien:
            x, y, ladung = batterie
            aktuelle_ladung_batterien[(x, y)] = ladung

        aktuelle_ladung_batterien[self.roboter[:2]] = self.roboter[2]

        #längster_pfad = self.bfs(self.graph, (self.roboter[:2]), self.roboter[2], aktuelle_ladung_batterien, self.batterien)

        # als Liste der restlichen Batterien werden nur die x- und y-Koordinaten aller Batterien benötigt
        restliche_batterien = list(
            map(lambda batterie: batterie[:2], self.batterien))

        längster_pfad = self.dfs(
            graph=self.graph,
            aktueller_knoten=self.roboter[:2],
            alte_ladung=0,
            a_alte_ladung=0,
            aktuelle_ladung_batterien=aktuelle_ladung_batterien)
        # )
        print("PFAD: ", längster_pfad)

        env = Environment(self.size, self.roboter, self.anzahl_batterien, self.batterien)
        env.step(0)
        pass

    def dfs(self, graph, aktueller_knoten, alte_ladung, a_alte_ladung, aktuelle_ladung_batterien, pfad=[]):
        """
            TODO
        """

        pfad.append(aktueller_knoten)
        print("Neuer Pfad: ", pfad)

        if len(pfad) > 1:
            # aktualisiere Nachbarknoten des vorherigen Knoten, da sich bei diesem die Ladung geändert hat

            # restliche_batterien.remove(start)

            alter_knoten = pfad[-2]
            # Aktualisierung des Dictionary zum Speichern der aktuellen Ladung
            aktuelle_ladung_batterien[alter_knoten] = a_alte_ladung

            # als Liste der restlichen Batterien werden nur die x- und y-Koordinaten aller Batterien benötigt, die aktuell eine Ladung > 0 besitzten
            # 1. Filtern der Batterien mit Ladung > 0
            restliche_batterien = list(filter(
                lambda batterie: batterie[1] > 0, list(
                    aktuelle_ladung_batterien.items())
            ))
            # 2. Nur die x- und y-Koordinaten werden benötigt
            restliche_batterien = list(
                map(lambda batterie: batterie[0], restliche_batterien))

            erreichbare_batterien_neu = self.erreichbareBatterien(
                *alter_knoten, a_alte_ladung, restliche_batterien)
            erreichbare_batterien_neu = list(map(
                lambda batterie: (*batterie, self.manhattanDistanz(
                    *batterie, *alter_knoten
                )), erreichbare_batterien_neu
            ))
            graph.aktualisiereNachfolger(
                alter_knoten, erreichbare_batterien_neu)

            #aktuelle_ladung_batterien[vorheriger_knoten] = aktuelle_ladung

            # if aktuelle_ladung > 0:
            #     restliche_batterien.append((*vorheriger_knoten, aktuelle_ladung))

            #aktuelle_ladung = aktuelle_ladung_batterien[aktueller_knoten]

            aktuelle_ladung = aktuelle_ladung_batterien[aktueller_knoten]

        else:
            # als Liste der restlichen Batterien werden nur die x- und y-Koordinaten aller Batterien benötigt, die aktuell eine Ladung > 0 besitzten
            # 1. Filtern der Batterien mit Ladung > 0
            restliche_batterien = list(filter(
                lambda batterie: batterie[1] > 0, list(
                    aktuelle_ladung_batterien.items())
            ))
            # 2. Nur die x- und y-Koordinaten werden benötigt
            restliche_batterien = list(
                map(lambda batterie: batterie[0], restliche_batterien))

            aktuelle_ladung = aktuelle_ladung_batterien[aktueller_knoten]

        # if graph[aktueller_knoten]:
        if len(restliche_batterien) == 1 and aktueller_knoten == restliche_batterien[0]:
            print("YESSS")
            return pfad

        # für benachbarte Knoten wird die DFS aufgerufen
        for nachfolger_item in graph[aktueller_knoten]:
            knoten, gewichtung = nachfolger_item[0]

            # falls der Knoten noch nicht besucht wurde
            if knoten in restliche_batterien:

                # Ladungsverbrauch wird abgezogen
                #aktuelle_ladung -= gewichtung

                p = self.dfs(graph=copy.deepcopy(graph), aktueller_knoten=knoten,
                             alte_ladung=(aktuelle_ladung-gewichtung),
                             a_alte_ladung=alte_ladung,
                             aktuelle_ladung_batterien=aktuelle_ladung_batterien,
                             pfad=pfad.copy())

                # print("Pfad: ", p)

                if p:
                    # pass
                    return p

            # # falls alle Batterien besucht wurden
            # elif not restliche_batterien:
            #     # return pfad
            #     #return pfad
            else:
                # return pfad
                if len(restliche_batterien) == 1 and aktueller_knoten == restliche_batterien[0]:
                    print("YESSS")
                    return pfad

        # else:
        #     return pfad

    def bfs(self, graph, aktueller_knoten, aktuelle_ladung_roboter, aktuelle_ladung_batterien, restliche_batterien, aktueller_pfad=[]):

        # # jetzt ändert sich eventuell die erreichbaren Batterien der aktuellen Ersatzbatterie, die ja eine neue Ladung bekommen
        #         erreichbare_batterien_neu = self.erreichbareBatterien(*knoten, aktuelle_ladung_roboter, restliche_batterien)
        #         graph.aktualisiereNachfolger(knoten, erreichbare_batterien_neu)

        if graph[aktueller_knoten]:

            for nachfolge_item in graph[aktueller_knoten]:
                # if knoten not in aktueller_pfad
                knoten, verbrauchte_ladung = nachfolge_item[0]

                aktueller_pfad.append(knoten)

                aktuelle_ladung_roboter -= verbrauchte_ladung

                # Ladungstausch: Bordbatterie des Roboters und aktuelle Ersatzbatterie werden getauscht
                # Ladung der Ersatzbatterie wird ermittelt
                batterie_am_boden = aktuelle_ladung_batterien[knoten]

                try:
                    # die aktuelle Batterie wird von den restlichen Batterien entfernt
                    restliche_batterien.remove((*knoten, batterie_am_boden))
                except:
                    pass

                # Ladung der Ersatzbatterie wird zur aktuellen Ladung des Roboters
                #aktuelle_ladung_batterien[knoten] = aktuelle_ladung_roboter

                # falls keine Batterien mehr übrig sind
                if not restliche_batterien:
                    if aktuelle_ladung_roboter > 0:
                        # TODO Ladung leer machen
                        pass
                    return aktueller_pfad

                # aktuelle_nachfolger = []
                # aktuelle_nachfolger_items = graph[knoten]
                # for item in aktuelle_nachfolger_items:
                #     k, g = item[0]
                #     aktuelle_nachfolger.append(k)

                # aktuelle Ladung des Roboters wird zur Ladung die am Boden lag, da der Roboter die Batterie am Boden aufnimmt
                #aktuelle_ladung_roboter = batterie_am_boden

                return self.bfs(graph, knoten, aktuelle_ladung_roboter, aktuelle_ladung_batterien, restliche_batterien, aktueller_pfad)

        else:
            return None

        pass


class Graph:
    """ Klasse gerichteter Graph zum Verwalten von Knoten und Kanten mit Gewichtungen """

    def __init__(self):
        """ erstellt ein leeres Dictionary zum Speichern des Graphen """
        self.adjazenzliste = defaultdict(list)

    def add_Kante(self, start, ende, gewichtung):
        """ fügt eine neue Kante zum Dictionary mit der gegebenen Gewichtung
            gerichteter Graph, daher muss die Kante nur einmal für den Startknoten hinzugefügt werden
        """
        self.adjazenzliste[start].append({
            ende: gewichtung
        })

    def delete_Kante(self, start, entfernendes_item):
        """ das zu entfernende Item wird aus der Liste des Startknoten entfernt
        """
        self.adjazenzliste[start].remove(entfernendes_item)

    @property
    def knoten(self):
        # TODO gilt für gerichteten Graphen nicht
        # TODO Zielknoten fehlen
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
        """ gibt die Nachfolgeknoten zusammen mit deren Gewichtungen zurück """
        return [list(n.items()) for n in self.adjazenzliste[key]]

    def aktualisiereNachfolger(self, knoten, neueNachfolger: list):
        """ updatet die Nachfolgerknoten des gegebenen Knoten:
            neue Nachfolger werden hinzugefügt, nicht mehr vorhandene werden entfernt
        """
        # hier muss .copy() verwendet werden, da sonst sich die Liste ursprüngliche_nachfolger_items
        # bei Entfernen von Knoten aus der Adjazenzliste verändert!
        ursprüngliche_nachfolger_items = self.adjazenzliste[knoten].copy()
        for nachfolger_item in neueNachfolger:

            # falls das Item nicht in den aktuellen Nachfolger Items ist,
            # muss dieses hinzugefügt werden
            if nachfolger_item not in ursprüngliche_nachfolger_items:
                x, y, gewichtung = nachfolger_item
                self.add_Kante(knoten, (x, y), gewichtung)

            else:
                ursprüngliche_nachfolger_items.remove(nachfolger_item)

        # falls noch Items übrig sind,
        # müssen diese entfernt werden
        if ursprüngliche_nachfolger_items:
            for item in ursprüngliche_nachfolger_items:
                self.delete_Kante(knoten, item)

UNIT = 40

class Environment(tk.Tk, object):

    def __init__(self, size: int, roboter: tuple, anzahl_batterien: int, batterien: list):
        """ erstellt eine Umgebung mit der gegebenen Eingabe """
   
        super(Environment, self).__init__()
        # Ausgangszustand wird gespeichert, damit die Umgebung wieder zurückgesetzt werden kann
        self.roboter_start = roboter
        self.batterien_start = batterien

        # TODO IWAS origin ?!
        self.origin = np.array([UNIT/2, UNIT/2])

        self.size = size

        # Batterien:
        self.anzahl_batterien = anzahl_batterien
        # die Batterien werden gesammelt in einem Dictionary ebenfalls wie der Roboter in der Form:
        # (x, y, ladung) gespeichert
        # wobei (x, y, ladung) als Key des Dictionary fungiert und die id des Text-Widgets von Tkinter der jeweilige Value ist
        # der Value wird später erstellt
        self.batterien = dict.fromkeys(batterien)

        # Die Positon des Roboters oder der Batterien werden in einem Dictionary mit der Form (x, y, ladung) gespeichert
        # Key ist (x, y, ladung) und der Value ist eine Liste mit der ID des grünen Quadrats (stellt den Roboter da) und mit der ID des Text-Widgets
        self.roboter = dict.fromkeys([roboter])

        self.action_space = [0, 1, 2, 3]
        self.n_actions = len(self.action_space)
        self.title('Stromrallye')
        self.geometry('{0}x{1}'.format(self.size * UNIT, self.size * UNIT))
        self._build_stromrallye()

    def _build_stromrallye(self):
        """ in dieser Methode wird das Spielbrett auf Ausgangsstellung auf einer Zeichenfläche (Canvas) gezeichnet """

        # Canvas objekt wird erstellt
        # weißer Hintergrund mit gegebener, quadratischer Größe des Spielbretts
        self.canvas = tk.Canvas(
            self, bg='white',
            height=self.size * UNIT,
            width=self.size * UNIT)

        # Gitter erstellen
        for spalte in range(0, self.size * UNIT, UNIT):
            x0, y0, x1, y1 = spalte, 0, spalte, self.size * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for reihe in range(0, self.size * UNIT, UNIT):
            x0, y0, x1, y1 = 0, reihe, self.size * UNIT, reihe
            self.canvas.create_line(x0, y0, x1, y1)

        # Ersatzbatterien mit aktuellem Akkustand zeichnen
        for key in self.batterien.keys():
            x, y, ladung = key

            # Mittelpunkt des Feldes der jeweiligen Ersatzbatterie
            batt_center = np.array([(x-1) * UNIT, (y-1) * UNIT]) + self.origin

            # gelbes Quadrat als Zeichen für eine Ersatzbatterie
            self.canvas.create_rectangle(
                batt_center[0] - 15, batt_center[1] - 15,
                batt_center[0] + 15, batt_center[1] + 15,
                fill='yellow'
            )

            # ein Text mit der Ladung der Batterie wird im Mittelpunkt des Feldes angezeigt
            # Value des Dictionary self.batterien wird mit der ID des Text-Widgets von Tkinter versehen
            self.batterien[key] = self.canvas.create_text(
                *batt_center, text=ladung)

        # Roboter zeichnen:
        x, y, ladung = list(self.roboter.keys())[0]
        robo_center = np.array([(x-1) * UNIT, (y-1) * UNIT]) + self.origin

        self.roboter[(x, y, ladung)] = []
        # grünes Quadrat als Zeichen für den Roboter
        # das grüne Quadrat wird mit dem Tag 'roboter' versehen, um später darauf zugreifen zu können
        self.roboter[(x, y, ladung)].append(self.canvas.create_rectangle(
            robo_center[0] - 15, robo_center[1] - 15,
            robo_center[0] + 15, robo_center[1] + 15,
            fill='green', tags=('roboter')
        ))

        # Text mit aktueller Ladung der Bordbatterie
        # das Text-Widget wird mit 'roboter_batterie' versehen
        self.roboter[(x, y, ladung)].append(self.canvas.create_text(
            *robo_center, text=f'{ladung}', tags=('roboter_batterie')
        ))

        # Canvas pack
        self.canvas.pack()
        self.focus()

    def _update_gui(self):
        """ aktualisiert die angezeigten Zahlen und die Position des Roboters auf dem GUI --> Rendert die Oberfläche"""
        time.sleep(0.1)
        # Roboter aktualisieren:
        # grünes Quadrat bewegen und die Zahl für die Ladung der Bordbatterie aktualisieren
        (x, y, ladung), [id_quadrat, id_text] = list(self.roboter.items())[0]
        # x- und y-Koordinate der alten Position
        old_coords = np.array(self.canvas.coords(id_quadrat)[0:2])
        new_coords = np.array([(x-1) * UNIT+5, (y-1) * UNIT+5])
        diff = new_coords - old_coords

        # Quadrat und Text um die Veränderung bewegen
        self.canvas.move(id_quadrat, *diff)
        self.canvas.move(id_text, *diff)

        # Anzeige der Ladung aktualisieren
        self.canvas.itemconfigure(id_text, text=ladung)

        # Akkuladungen der Ersatzbatterien wird aktualisiert
        for item in self.batterien.items():
            (x, y, ladung), id = item
            self.canvas.itemconfigure(id, text=ladung)

        # die Position des Roboters wird aktualisiert
        # self.canvas.move()

        self.canvas.pack()
        self.update()

    def reset(self):
        self.update()
        time.sleep(0.5)
        # Tkinter Fenster wird geschlossen
        self.canvas.destroy()
        # Ausgangszustand wird wiederhergestellt
        self.__init__(self.size, self.roboter_start, self.anzahl_batterien, self.batterien_start)
        self._build_stromrallye()

        (x_robo, y_robo, ladung_roboter) = list(self.roboter.keys())[0]

        # gib Observation zurück
        state = [
            (x_robo, y_robo, ladung_roboter),
            (list(self.batterien.keys()))
        ]
        return state

    def step(self, action: int):
        """ bewegt den Roboter in der Umgebung
            nach oben: 0
            nach unten: 1
            nach links: 2
            nach rechts: 3
        """
        against_wall = False
        reward = 0

        # speichert den auszuführenden Vorgang
        #base_action = np.array([0, 0])
        (x_robo, y_robo, ladung_roboter), id_liste = list(self.roboter.items())[0]
        self.roboter.pop((x_robo, y_robo, ladung_roboter))

    
        # wenn die Ladung für einen Schritt ausreicht
        # TODO:
        # Roboter an Wand und kann sich nicht mehr weiter bewegen +
        # negativer Reward bei Laufen gegen die Wand
        if action == 0:
            if y_robo > 1:
                # hoch: y-Koordinate -1
                y_robo -= 1
            else:
                # neg. Reward
                against_wall = True

        elif action == 1:
            if y_robo < self.size:
                # runter: y-Koordinate +1
                y_robo += 1
            else:
                # neg. Reward
                against_wall = True

        elif action == 2:
            if x_robo > 1:
                # links: x-Koordinate -1
                x_robo -= 1
            else:
                # neg. Reward
                against_wall = True

        elif action == 3:
            if x_robo < self.size:
                # rechts: x-Koordinate +1
                x_robo += 1
            else:
                # neg. Reward
                against_wall = True

        print("ladung : ", ladung_roboter)

        if ladung_roboter > 0:
            if against_wall:
                # reward += REWARD_WALL            
                pass
            else:
                # Schritt ist möglich
                # positiver Reward und Ladung der Bordbatterie -1
                # reward += REWARD_STEP
                ladung_roboter -= 1                              

            done = False

        else:
            # Schritt ist aufgrund der Ladung der Bordbatterie des Roboters nicht mehr möglich
            # reward += REWARD_FAILED
            done = True

        if max([ladung[2] for ladung in self.batterien.keys()]) == 0 and ladung_roboter == 0:
            print("Max Ladung Batterien", max([ladung[2] for ladung in self.batterien.keys()]))
            # höchste Ladung der Ersatzbatterien ist 0 und die Ladung des Roboters ist auf 0
            # Spiel fertig gelöst
            # reward += REWARD_FINISH   
            done = True 
    
        

        # Aktualisierung der Klassenvariable
        self.roboter[(x_robo, y_robo, ladung_roboter)] = id_liste
        #self._update_gui()

        # Überprüfung, ob sich der Roboter jetzt auf einem Feld mit einer Ersatzbatterie befindet
        for koordinaten, ladung_batterie in zip([koordinaten[0:2] for koordinaten in self.batterien.keys()], [ladung[2] for ladung in self.batterien.keys()]):
            if (x_robo, y_robo) == koordinaten:
                self.batterien[(x_robo, y_robo, ladung_roboter)] = self.batterien.pop(
                    (x_robo, y_robo, ladung_batterie))
                self.roboter[(x_robo, y_robo, ladung_batterie)] = self.roboter.pop(
                    (x_robo, y_robo, ladung_roboter))
        
        self._update_gui()

        new_state = np.array([
            (x_robo, y_robo, ladung_roboter),
            (list(self.batterien.keys()))
        ])
        print(f">> Neuer State: {new_state} >> Reward: {reward} >> Fertig? {done}" )
        print("Size: ", new_state.shape)
        return new_state, reward, done



if __name__ == '__main__':
    eingabe1 = """
    5
    3,5,9
    3
    5,1,3
    1,2,2
    5,4,3
    """.split()
    
    eingabe2= """ 
    10
    1,1,1
    99
    1,2,1
    1,3,1
    1,4,1
    1,5,1
    1,6,1
    1,7,1
    1,8,1
    1,9,1
    1,10,1
    2,1,1
    2,2,1
    2,3,1
    2,4,1
    2,5,1
    2,6,1
    2,7,1
    2,8,1
    2,9,1
    2,10,1
    3,1,1
    3,2,1
    3,3,1
    3,4,1
    3,5,1
    3,6,1
    3,7,1
    3,8,1
    3,9,1
    3,10,1
    4,1,1
    4,2,1
    4,3,1
    4,4,1
    4,5,1
    4,6,1
    4,7,1
    4,8,1
    4,9,1
    4,10,1
    5,1,1
    5,2,1
    5,3,1
    5,4,1
    5,5,1
    5,6,1
    5,7,1
    5,8,1
    5,9,1
    5,10,1
    6,1,1
    6,2,1
    6,3,1
    6,4,1
    6,5,1
    6,6,1
    6,7,1
    6,8,1
    6,9,1
    6,10,1
    7,1,1
    7,2,1
    7,3,1
    7,4,1
    7,5,1
    7,6,1
    7,7,1
    7,8,1
    7,9,1
    7,10,1
    8,1,1
    8,2,1
    8,3,1
    8,4,1
    8,5,1
    8,6,1
    8,7,1
    8,8,1
    8,9,1
    8,10,1
    9,1,1
    9,2,1
    9,3,1
    9,4,1
    9,5,1
    9,6,1
    9,7,1
    9,8,1
    9,9,1
    9,10,1
    10,1,1
    10,2,1
    10,3,1
    10,4,1
    10,5,1
    10,6,1
    10,7,1
    10,8,1
    10,9,1
    10,10,1
    """.split()
    
    eingabe3="""
    11
    6,6,2
    120
    1,1,2
    1,2,2
    1,3,2
    1,4,2
    1,5,2
    1,6,2
    1,7,2
    1,8,2
    1,9,2
    1,10,2
    1,11,2
    2,1,2
    2,2,2
    2,3,2
    2,4,2
    2,5,2
    2,6,2
    2,7,2
    2,8,2
    2,9,2
    2,10,2
    2,11,2
    3,1,2
    3,2,2
    3,3,2
    3,4,2
    3,5,2
    3,6,2
    3,7,2
    3,8,2
    3,9,2
    3,10,2
    3,11,2
    4,1,2
    4,2,2
    4,3,2
    4,4,2
    4,5,2
    4,6,2
    4,7,2
    4,8,2
    4,9,2
    4,10,2
    4,11,2
    5,1,2
    5,2,2
    5,3,2
    5,4,2
    5,5,2
    5,6,2
    5,7,2
    5,8,2
    5,9,2
    5,10,2
    5,11,2
    6,1,2
    6,2,2
    6,3,2
    6,4,2
    6,5,2
    6,7,2
    6,8,2
    6,9,2
    6,10,2
    6,11,2
    7,1,2
    7,2,2
    7,3,2
    7,4,2
    7,5,2
    7,6,2
    7,7,2
    7,8,2
    7,9,2
    7,10,2
    7,11,2
    8,1,2
    8,2,2
    8,3,2
    8,4,2
    8,5,2
    8,6,2
    8,7,2
    8,8,2
    8,9,2
    8,10,2
    8,11,2
    9,1,2
    9,2,2
    9,3,2
    9,4,2
    9,5,2
    9,6,2
    9,7,2
    9,8,2
    9,9,2
    9,10,2
    9,11,2
    10,1,2
    10,2,2
    10,3,2
    10,4,2
    10,5,2
    10,6,2
    10,7,2
    10,8,2
    10,9,2
    10,10,2
    10,11,2
    11,1,2
    11,2,2
    11,3,2
    11,4,2
    11,5,2
    11,6,2
    11,7,2
    11,8,2
    11,9,2
    11,10,2
    11,11,2
    """.split()
    
    
    eingabe5 = """
    20
    10,15,20
    34
    14,15,10
    18,15,4
    18,18,2
    18,20,10
    14,9,2
    5,7,2
    5,5,2
    5,3,2
    4,4,2
    4,6,2
    4,8,1
    4,9,5
    3,8,1
    2,8,1
    1,8,1
    1,9,1
    1,10,1
    1,11,1
    1,12,3
    1,13,1
    1,14,1
    1,15,1
    1,16,1
    1,17,1
    1,18,1
    2,17,1
    2,18,3
    2,19,1
    3,17,1
    3,18,1
    3,19,1
    4,17,1
    4,18,1
    4,19,1
    """.split()
    
    size = 5
    roboter = (3, 5, 9)
    anzahl_batterien = 3
    batterien = [
        (5, 1, 3),
        (1, 2, 2),
        (5, 4, 3),
        #(4, 3, 2)
    ]

    s = Steuerung(eingabe1)
