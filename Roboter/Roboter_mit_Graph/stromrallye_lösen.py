# 2. Runde Bundeswettbewerb Informatik 2019/20
# Autor: Christoph Waffler
# Aufgabe 1: Stromrallye

from collections import defaultdict
import copy
import numpy as np
import time

import sys
import random
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk
import math

class Steuerung:
    def __init__(self, eingabe: list):
        print(eingabe)
        # Größe des quadratischen Spielfelds
        self.size = int(eingabe.pop(0))

        # Aufbau: (x, y, ladung)
        self.roboter = self.zuPunkt(eingabe.pop(0))

        self.anzahl_batterien = int(eingabe.pop(0))

        # Aufbau: [(x1, y1, ladung1), (x2, y2, ladung2), ...]
        self.batterien = [self.zuPunkt(eingabe.pop(0))
                          for i in range(self.anzahl_batterien)]

        self.main()

    def zuPunkt(self, eingabe: str):
        """ Methode zur Formatierung einer Zeile aus der Eingabe mit Strings
        
        Args:
            eingabe (str): String mit unformatierter Eingabe, Aufbau der Eingabe: 'x, y, ladung'
        
        Returns:
            ein Tuple mit der x-, y-Koordinate und der Ladung, die als int dargestellt werden            
        """
        # erste Stelle des Kommas wird bestimmt
        ind_komma_1 = eingabe.find(',', 0, -1)

        # die x-Koordinate wird durch die Ziffern bis zum ersten Komma dargestellt
        x = int(eingabe[0:ind_komma_1])

        # die zweite Stelle des Kommas wird bestimmt
        ind_komma_2 = eingabe.find(',', ind_komma_1+1, -1)

        # die y-Koordinate wird durch die Ziffern vom ersten Komma bis zum zweiten Komma dargestellt
        y = int(eingabe[ind_komma_1 + 1: ind_komma_2])

        # die Ladung wird durch die Ziffern vom zweiten Komma bis zum Ende dargestellt
        ladung = int(eingabe[ind_komma_2 + 1:])
        
        # Ein Tuple aus x, y und Ladung wird zurückgegeben
        return (x, y, ladung)

    def erreichbareBatterien(self, x_start: int, y_start: int, ladung: int, restliche_batterien: list):
        """ Mithilfe der Manhattan-Distanz werden alle Batterie ermittelt,
            die von dem gegebenen Punkt aus erreichbar sind.
            
            Der Betrag der Manhattan-Distanz wird über eine eigene Methode berechnet. 
            Dieser gibt in dieser Aufgabe Auskunft darüber, wie viel Ladung zur Ersatzbatterie benötigt wird
            
            Args:
                x (int): x-Koordinate des Punkts
                y (int): y-Koordinate des Punkts
                ladung (int): maximale verbrauchbare Ladung
                
                restliche_batterien (list): Liste mit den Batterien, welche überprüft werden sollen, ob sie erreicht werden können.
                
            Returns:
                eine Liste mit den Batterien, die erreicht werden können
        """
                
        # Die gegebene Ladung ist der maximal mögliche Betrag der Manhattan-Distanz
        # daher werden alle Batterien herausgefiltert, dessen Manhattan-Distanz größer als die gegebene Ladung ist.
        # Zudem muss die Distanz größer als 0 sein, damit der Ausgangspunkt sich nicht selbst als erreichbare Batterie sehen kann
        if ladung > 0:
            erstauswahl = list(filter(
                lambda batterie_item: self.manhattanDistanz(x_start, y_start, batterie_item[0], batterie_item[1]) <= ladung 
                and self.manhattanDistanz(x_start, y_start, batterie_item[0], batterie_item[1]) > 0, restliche_batterien
            ))
            
            
            # Falls für den Weg von dem gegebenen Startpunkt zur Batterie in der Liste erstauswahl keine Schritte über Felder existieren,
            # ist die Batterie nicht erreichbar und wird von der Liste entfernt.
            erreichbare_batterien = list(filter(
                lambda batterie_item: self.findeWeg(x_start, y_start, *batterie_item[:2]) != None, erstauswahl
            ))
            
            # eine Liste mit erreichbaren Batterien wird zurückgegeben
            return erreichbare_batterien
            
        # Falls die Ladung <= 0 ist, wird eine leere Liste zurückgegeben, da keine Batterien erreicht werden können
        else:
            return []

    def manhattanDistanz(self, x1: int, y1: int, x2: int, y2: int):
        """ Methode zur Berechnung der Manhattan-Distanz zweier Punkte P1 und P2, 
            die sich auf einem Schbrettmuster-artigen Spielfeld befinden.
            Selbiges liegt auch in unserer Aufgabe vor.
            
            Bei der Manhattan-Distanz wird die Summe der Beträge der Differenz der x- und y-Koordinaten berechnet.
            
            Diese Distanz spiegelt somit die Distanz wieder, die man zurücklegen muss, 
            wenn man nur nach oben, rechts, unten oder links gehen kann.
            
            Bei dieser Aufgabe wird diese Art der Distanzberechnung verwendet, um berechnen zu können, 
            wie viel Ladung benötigt wird, um von einem Punkt zu einem anderen zu gelangen.
            
            Args:
                x1 (int): x-Koordinate von P1
                y1 (int): y-Koordinate von P1
                x2 (int): x-Koordinate von P2
                y2 (int): y-Koordinate von P2
            
            Returns:
                int. Manhattan-Distanz zwischen P1 und P2
        
        """
        # Betrag der Differenzen der x- und y-Koordinaten
        delta_x = abs(x1 - x2)
        delta_y = abs(y1 - y2)
        
        # Summe der Beträge wird gebildet
        distanz = delta_x + delta_y
        
        return distanz
        
    def abwägung(self, x: int, y: int, batterien_aktuelle_ladung: dict):
        """ Heuristische Funktion zum Abschätzen, welcher Knoten bei der DFS als nächster ausgewählt werden soll
            --> Liefert einen Wert, der mit den anderen Nachbarn verglichen werden kann
        """
        """ Diese Methode dient als Optimierung der Tiefensuche (depth-first-search, DFS).
        
        Diese Methode liefert einen Wert, der die Auswahl zwischen den Kinderknoten eines Knoten eines Graphen optimieren soll.
        
        Dabei wird der Wert zwischen den Kinderknoten verglichen 
        und die Suche wird mit dem Kinderknoten mit dem maximialen Wert fortgesetzt.
        
        Der Wert wird von zwei Faktoren beeinflusst: 
            - Ladung der Batterie (des aktuellen Kinderknoten)
            - Abstand zum Startpunkt des Roboters
        
        Die Ladung der aktuellen Batterie (=Kinderknoten) wird mithilfe des gegebenen Dictionary ermittelt.
        
        Da der diejenigen Knoten priorisiert werden sollen, die eine höhere Ladung haben, wird der Wert der Ladung quadriert.
        Somit ist der Betrag der Ladung gegenüber dem Abstand zum Roboter höher gewichtet
        
        Args:
            x (int): x-Koordinate des aktuellen Knoten
            y (int): y-Koordinate des aktuellen Knoten
            
            batterien_aktuelle_ladung (dict): Dictionary mit den aktuellen Ladungsständen der Batterien

        Returns:
            float. heuristischer Wert zum Vergleichen 
        """        
        
        # x- und y-Koordinate des Startpunktes des Roboters werden benötigt
        roboter = self.roboter[:2]
        
        # euklidischer Abstand wird verwendet
        abstand = self.euklidischerAbstand(x, y, *roboter)
        
        # aktuelle Ladung der Batterie wird ausgelesen
        aktuelle_ladung_batterie = batterien_aktuelle_ladung[(x, y)]
        
        # das Produkt aus dem Abstand und dem Quadrat der Ladung wird zurückgegeben
        return  aktuelle_ladung_batterie**2 * abstand
            
    def euklidischerAbstand(self, x1: int, y1: int, x2: int, y2: int):
        """ Methode zur Berechnung des euklidischen Abstands zwischen zwei Punkten P1 und P2.
        
        Der Abstand wird mithilfe des Satzes von Pythagoras berechnet.
        Somit gilt:
            - Zuerst werden die Differenzen der x- und y-Koordinaten berechnet.
            - Anschließend wird die Wurzel aus dem Quadrat der jeweiligen Differenzen gezogen.
            - Dieser Betrag spiegelt den euklidischen Abstand wieder.
        
        Args:
            x1 (int): x-Koordinate von P1
            y1 (int): y-Koordinate von P1
            x2 (int): x-Koordinate von P2
            y2 (int): y-Koordinate von P2
            
        Returns:
            float. euklidischen Abstand zwischen P1 und P2        
        """
        
        delta_x = x2 - x1
        delta_y = y2 - y1
        distanz = math.sqrt(delta_x**2 + delta_y**2)
        return distanz
    

    def main(self):
        """ Hauptmethode des gesamten Programms
        """
        # ein Graph der Klasse Graph wird erzeugt
        self.graph = Graph()
        
        # zu diesem Graphen wird für jede Ersatzbatterie alle erreichbaren, anderen Ersatzbatterien zum Graphen hinzugefügt
        for batterie in self.batterien:
            
            # eine Kopie der Liste wrid erstellt, von der die aktuelle Batterie entfernt wird
            restliche_batterien = self.batterien.copy()
            restliche_batterien.remove(batterie)
            
            # alle erreichbaren Batterien werden ermittelt
            erreichbare_batterien = self.erreichbareBatterien(*batterie, restliche_batterien)
           
            for erreichbare_batterie in erreichbare_batterien:                
                # die erreichbaren Batterien bilden zusammen mit der aktuellen Batterie eine Kante,                
                # wobei die aktuelle Batterie der Startknoten der Kante und die erreichbare Batterie der Endknoten der Kante ist    
                
                # nur die x- und y-Koordinaten der Batterien werden benötigt, die Ladung der Batterien nicht
                x_start, y_start = batterie[:2]
                x_ende, y_ende = erreichbare_batterie[:2]

                # verbrauchte Ladung ist die Manhattan-Distanz
                verbrauchte_ladung = self.manhattanDistanz(
                    x_start, y_start, x_ende, y_ende)
                
                # die Gewichtung der Kante ist die verbrauchte Ladung von der aktuellen Batterie zur erreichbaren Batterie                
                # Kante wird zum Graphen hinzugefügt
                self.graph.add_Kante((x_start, y_start),
                                     (x_ende, y_ende), verbrauchte_ladung)

        
        # Dasselbe wird ebenfalls für den Roboter durchgeführt:
        
        # Erreichbare Batterien werden ermittelt
        roboter_erreichbare_batterien = self.erreichbareBatterien(*self.roboter, self.batterien)
        for erreichbare_batterie in roboter_erreichbare_batterien:
            x_start, y_start = self.roboter[:2]
            x_ende, y_ende = erreichbare_batterie[:2]

            verbrauchte_ladung = self.manhattanDistanz(
                x_start, y_start, x_ende, y_ende)
            
            # Kante wird zum Graphen hinzugefügt
            self.graph.add_Kante((x_start, y_start),
                                 (x_ende, y_ende), verbrauchte_ladung)

        # Ein Dictionary zum Speichern der aktuellen Ladungen der Batterien wird erstellt
        aktuelle_ladung_batterien = defaultdict(list)
        for batterie in self.batterien:
            x, y, ladung = batterie
            # x- und y-Koordinate stellen den Key eines Elements im Dictionary dar
            aktuelle_ladung_batterien[(x, y)] = ladung

        # auch die Startladung des Roboters wird zum Dictionary hinzugefügt
        aktuelle_ladung_batterien[self.roboter[:2]] = self.roboter[2]
        
        
        # Ein Pfad wird mit der Methode dfs ermittelt, 
        # welcher die Route des Roboters angibt, damit alle Batterien am Ende leer sind
        
        # Der Pfad beinhaltet die Punkte auf dem Spielbrett, zu welchem der Roboter geht.
        # Am Ende hat der Roboter noch eine restliche Ladung, welche die Methode dfs ebenfalls zurückgibt.
        
        # die restliche Ladung wird später dann noch "verbraucht".
        pfad, restliche_ladung = self.dfs(
            graph=self.graph,
            aktueller_knoten=self.roboter[:2],
            alte_ladung=0,
            a_alte_ladung=0,
            aktuelle_ladung_batterien=aktuelle_ladung_batterien)
        
        print(">> Pfad gefunden > ", pfad)
        
        # die Abfolge der Schritte des Roboters werden aus dem Pfad ermittelt
        # mögliche Schritte sind: nach oben, rechts, unten und links
        
        # in abfolge_schritte werden die Schritte für den gesamten Pfad gespeichert
        abfolge_schritte = []
        for i in range(len(pfad)):
            if i > 0:
                
                # zwei aufeinanderfolgende Punkte spiegeln einen Teilweg des Pfades wieder
                p1 = pfad[i-1]
                p2 = pfad[i]

                # die Methode findeWeg gibt eine mögliche Abfolge der Schritte für diesen Teilweg zurück
                # die möglichen Schritte werden als Zahl dargestellt. (Näheres ist der Methode findeWeg oder der Dokumentation zu entnehmen)
                schritte = self.findeWeg(*p1, *p2)
                
                # die Schritte für den Teilweg werden zu abfolge_schritte hinzugefügt
                abfolge_schritte.extend(schritte)

        # als Liste der restlichen Batterien werden nur die x- und y-Koordinaten aller Batterien benötigt
        batterien_x_y = list(
            map(lambda batterie: batterie[:2], self.batterien))

        # zu der Abfolge der Schritten kommen noch diejenigen Schritte hinzu,
        # die benötigt werden, um die restliche Ladung zu entladen, die der Roboter zum Schluss noch besitzt
        if restliche_ladung > 0:
            letzte_position = pfad[-1]
            nachbarn1 = self.findeFreieNachbarpunkte(
                *letzte_position, batterien_x_y)

            # Prüfen, ob eine Zahl in der Liste ist
            if any(isinstance(item, int) for item in nachbarn1):
                erster_nachbar = nachbarn1.sort(
                    key=lambda x: (x is None, x))[0]
                nachbarn2 = self.findeFreieNachbarpunkte(
                    *erster_nachbar, batterien_x_y)
                if any(isinstance(item, int) for item in nachbarn2):
                    zweiter_nachbar = nachbarn2.sort(
                        key=lambda x: (x is None, x))[0]

                    # Schritt von letzter Position zum ersten Nachbarn
                    von_letzter_pos_zu_nachbar1 = self.findeWeg(
                        *letzte_position, *erster_nachbar)[0]

                    # Schritt vom ersten Nachbarn zum zweiten Nachbarn
                    von_nachbar1_zu_nachbar2 = self.findeWeg(
                        *erster_nachbar, *zweiter_nachbar)[0]

                    # Schritt vom zweiten Nachbarn zum ersten
                    von_nachbar2_zu_nachbar1 = self.findeWeg(
                        *zweiter_nachbar, *erster_nachbar)[0]

                    abfolge_schritte.append(von_letzter_pos_zu_nachbar1)
                    restliche_ladung -= 1
                    aktuelle_position = erster_nachbar

                    # Solange der Roboter noch Ladung besitzt,
                    # geht dieser immer vom ersten Nachbarn zum zweiten und wieder zurück
                    # Er geht sozusagen immer hin und her
                    while restliche_ladung > 0:

                        # wenn sich der Roboter gerade auf dem Feld des ersten Nachbarn befindet
                        # so geht er vom ersten zum zweiten Nachbarn
                        if aktuelle_position == erster_nachbar:
                            abfolge_schritte.append(von_nachbar1_zu_nachbar2)
                            aktuelle_position = zweiter_nachbar

                        # wenn sich der Roboter gerade auf dem Feld des zweiten Nachbarn befindet
                        # so geht er vom zweiten wieder zum ersten Nachbarn
                        else:
                            abfolge_schritte.append(von_nachbar2_zu_nachbar1)
                            aktuelle_position = erster_nachbar

                        restliche_ladung -= 1
            # TODO Beispiel2

            else:
                if restliche_ladung == 1:

                    # Wenn am oberen Rand (also y-Koordinate gleich 1)
                    # Schritt nach unten
                    if letzte_position[1] == 1:
                        abfolge_schritte.append(1)

                    # sonst Schritt nach oben
                    else:
                        abfolge_schritte.append(0)

        # for i in range(len(längster_pfad)):
        #     if i > 0:
        #         anfang = längster_pfad[i-1]
        #         ende = längster_pfad[i]

        #         delta_x = ende[0] - anfang[0]
        #         delta_y = ende[1] - anfang[1]

        #         neuer_punkt = anfang
        #         for j in range(abs(delta_x)):
        #             neuer_punkt[0] + j

        #             neuer_punkt in batterien_x_y:
        #                 neuer_punkt[1] + 1
        #                 delta_y -= 1

        #         for j in range(delta_y):
        #             neuer_punkt[]

        env = Environment(self.size, self.roboter,
                          self.anzahl_batterien, self.batterien)
        for schritt in abfolge_schritte:
            env.step(schritt)
            env.update()
        pass

    def findeWeg(self, x_start, y_start, x_ziel, y_ziel):
        """ Methode zum Ermitteln der Abfolge der Schritte vom Start- zum Zielpunkt.
                
        Die Datenstruktur Graph wird eingesetzt. 
        Es wird zuerst der Bereich des Spielfelds eingrenzt, in dem Suche stattfinden soll.
        Dies Außengrenzen des Bereich sind durch die Koordinaten des Start- und Zielpunkts definiert.
        
        Für jeden Punkt in diesem Bereich wird nun dessen Nachbarpunkte als Kante zum Graphen hinzugefügt.
        Die Nachbarpunkte werden mithilfe der Methode findeFreieNachbarpunkte() ermittelt.
        
        Mithilfe des A*-Algorithmus wird aus dem erstellten Graph der kürzeste Weg vom gegebene Startpunkt zum Zielpunkt gefunden.
        Dieser Weg besteht aus einzelnen Feldern des Spielfelds.
        
        Zu beachten ist dabei, dass auf Feldern des Wegs keine Batterien liegen.
        
        Die möglichen Schritte werden wie folgt als Zahl dargestellt:
            - nach oben: 0
            - nach unten: 1
            - nach links: 2
            - nach rechts: 3
        
        Args:
            x_start (int): x-Koordinate des Startpunktes
            y_start (int): y-Koordinate des Startpunktes
            
            x_ziel (int): x-Koordinate des Zielpunktes
            y_ziel (int): y-Koordinate des Zielpunktes
        
        Returns:
            list. Liste mit Abfolge von Schritten vom Start- zum Zielpunkt über einzelne Felder,
                die untereinander erreicht werden können. Die Schritte sind als Zahl dargestellt.
        """
        # Die Differenzen der x- und y-Koordinaten werden zur Eingrenzung des Bereichs berechnet                
        delta_x = x_ziel - x_start
        delta_y = y_ziel - y_start

        # nur die x- und y-Koordinaten aller Batterien werden benötigt
        batterien_x_y = [batterie[0:2] for batterie in self.batterien]
                
        # Start- und Zielpunkt sollen im nachfolgenden Algorithmus nicht als potenzielles Hindernis gespeichert werden
        # da der Algorithmus sonst keinen Weg finden würde, wenn beispielsweise der Zielpunkt in der Liste der potenziellen Hindernisse gespeichert wird
        startpunkt, zielpunkt = (x_start, y_start), (x_ziel, y_ziel)
        if startpunkt in batterien_x_y:
            batterien_x_y.remove(startpunkt)
        if zielpunkt in batterien_x_y:
            batterien_x_y.remove(zielpunkt)

        graph = Graph()

        aktuelle_position = [x_start, y_start]
        
        # step gibt die Richtung an, in der über den Bereich iteriert wird.
        # Der Bereich ist durch die Koordinaten des Start- und Zielpunkts definiert.
        
        # ein step ist entweder bei positivem Delta +1, bei negativem Delta -1        
        # bei +1 wird von links nach rechts iteriert, bei -1 umgekehrt
        if delta_y > 0:
            step_y = 1
        else:
            step_y = -1
        
        if delta_x > 0:
            step_x = 1
        else:
            step_x = -1


        # for-Schleife iteriert von y_start bis einschließliche y_ziel, mit step_y als Schritt (entweder +1 oder -1)
        for i in range(y_start, y_ziel + step_y, step_y):
            aktuelle_position[1] = i

            # analog zur for-Schleife für die y-Koordinate, diesmal in x-Richtung
            for j in range(x_start, x_ziel + step_x, step_x):
                aktuelle_position[0] = j

                nachbarn = self.findeFreieNachbarpunkte(
                    *aktuelle_position, batterien_x_y)

                for punkt in nachbarn:
                    # falls punkt nicht NoneType ist
                    if punkt:
                        graph.add_Kante(
                            tuple(aktuelle_position), punkt, 1)

        return_item = self.astar((x_start, y_start), (x_ziel, y_ziel), graph)

        # falls überhaupt ein Weg gefunden wurde
        if return_item:
            kürzester_weg, länge = return_item
            abfolge_schritten = []

            for index in range(len(kürzester_weg)):
                if index > 0:
                    # Teilweg aus den Punkten P1 und P2
                    p1 = kürzester_weg[index-1]
                    p2 = kürzester_weg[index]
                    
                    # die Differenzen der x- und y-Koordinaten wird berechnet
                    delta_x = p2[0] - p1[0]
                    delta_y = p2[1] - p1[1]

                    # je nach Differenz der Koordinaten muss eine bestimmte Bewegung ausgeführt werden (z. B. nach rechts gehen),
                    # um von P1 zu P2 zu gelangen
                
                    # nach rechts
                    if delta_x > 0:
                        bewegung = 3

                    # nach links
                    elif delta_x < 0:
                        bewegung = 2

                    # nach unten
                    elif delta_y > 0:
                        bewegung = 1

                    # nach oben
                    elif delta_y < 0:
                        bewegung = 0

                    abfolge_schritten.append(bewegung)
            # TODO
            print(
                f"> Weg von {(x_start, y_start)} zu {(x_ziel, y_ziel)} bei > Abfolge von Schritten: {abfolge_schritten}")
            return abfolge_schritten
        else:
            return None

    def findeFreieNachbarpunkte(self, x_akt, y_akt, potenzielle_hindernisse):
        """ Findet von den gegebenen x- und y-Koordinaten alle erreichbare Nachbarpunkte,
            welcher nicht als potenzielles Hindernis gespeichert ist
            Return liste mit erreichbaren Nachbarpunkten             
        """
        """ Methode zum Ermitteln freier nachbarpunkte.
        
        Diese prüft ob die Nachbarpunkte des gegebenen Punktes frei sind, d.h. dass dort keine Ersatzbatterien sind.
        Überprüft werden dabei:
            - Punkt oberhalb
            - Punkt unterhalb
            - Punkt rechts davon
            - Punkt links davon 
            (falls vorhanden).
            
        Da Punkte an den Rändern bzw. in den Ecken des Spielfelds nicht alle Nachbarpunkte haben können, 
        wird die Überprüfung durch if-Bedingungen gestützt, die vorliegende Postion des gegebenen Punktes eingrenzen.
        
        Args:
            x (int): x-Koordinate des Punktes
            y (int): y-Koordinate des Punktes
            potenzielle_hindernisse (list): Liste mit möglichen Hindernissen
        
        Returns:
            list. Liste mit freien Nachbarpunkten, auf denen kein Hindernis ist, welche somit erreichbar sind.
        """       
        # Aktuelle Postion ist durch die gegebenen x- und y-Koordinaten definiert.
        aktuelle_position = [x_akt, y_akt]

        if aktuelle_position not in potenzielle_hindernisse:
                        
            # in der Liste nachbarn werden alle erreichbaren Nachbarpunkte gespeichert
            nachbarn = []

            # Dabei wird die aktuelle Position kopiert, und die Koordinate entsprechend dem Nachbarpunkt verändert.
            # damit sich die Liste des jeweiligen Nachbarpunktes (z.B. unten) bei Veränderung von der aktuellen Position nicht verändert.
            
            # Die Nachbarpunkte werden als Tuple gespeichert, damit diese für die Datenstruktur des Graphen hashable sind.
            
            # bei dem unteren Nachbarpunkt wird die y-Koordinate um 1 erhöht
            unten = aktuelle_position.copy()
            unten[1] += 1
            unten = tuple(unten)
            if unten in potenzielle_hindernisse:
                unten = None

            # linker Nachbarpunkt: x-Koordinate -1
            links = aktuelle_position.copy()
            links[0] -= 1
            links = tuple(links)
            if links in potenzielle_hindernisse:
                links = None

            # rechter Nachbarpunkt: x-Koordinate +1
            rechts = aktuelle_position.copy()
            rechts[0] += 1
            rechts = tuple(rechts)
            if rechts in potenzielle_hindernisse:
                rechts = None

            # oberer Nachbarpunkt: y-Koordinate -1
            oben = aktuelle_position.copy()
            oben[1] -= 1
            oben = tuple(oben)
            if oben in potenzielle_hindernisse:
                oben = None

            # In dieser Aufgabe ist die minimale Koordinate 1 
            # und die maximale Koordinate die Größe des Spielfelds

            # aktuelle Position ist ganz oben links (Eckpunkt)
            # erreichbare Nachbarpunkte sind daher rechts und unten
            if y_akt == 1 and x_akt == 1:
                nachbarn.extend((rechts, unten))

            # aktuelle Position ist ganz oben rechts (Eckpunkt)
            # erreichbare Nachbarpunkte sind unten und links
            elif y_akt == 1 and x_akt == self.size:
                nachbarn.extend((unten, links))

            # aktuelle Position ist ganz oben am Rand und in keiner Ecke
            # erreichbare Nachbarpunkte sind unten, links, rechts
            elif y_akt == 1:
                nachbarn.extend((unten, links, rechts))

            # aktuelle Position ist ganz unten rechts (Eckpunkt)
            # erreichbare Nachbarpunkte sind oben und links
            elif y_akt == self.size and x_akt == self.size:
                nachbarn.extend((oben, links))

            # aktuelle Position ist ganz unten links (Eckpunkt)
            # erreichbare Nachbarpunkte sind oben und rechts
            elif y_akt == self.size and x_akt == 1:
                nachbarn.extend((oben, rechts))

            # aktuelle Position ist ganz unten am Rand und in keiner Ecke
            # erreichbare Nachbarpunkte sind oben, rechts und links
            elif y_akt == self.size:
                nachbarn.extend((oben, rechts, links))

            # aktuelle Position ist ganz rechts am Rand und in keiner Ecke
            # erreichbare Nachbarpunkte sind oben, unten und links
            elif x_akt == self.size:
                nachbarn.extend((oben, unten, links))

            # aktuelle Position ist ganz links am Rand und in keiner Ecke
            # erreichbare Nachbarpunkte sind oben, unten und rechts
            elif x_akt == 0:
                nachbarn.extend((oben, unten, rechts))

            # die aktuelle Position befindet sich nicht am Rand und auch in keiner Ecke
            # erreichbare Nachbarpunkte sind oben, unten, rechts und unten
            else:
                nachbarn.extend((oben, unten, rechts, links))

            return nachbarn

    def astar(self, start, ziel, graph):
        """ A*-Algorithmus zur Berechnung des kürzesten Weg.
        
        Im gegebenen Graph soll vom Start- zum Zielknoten der kürzeste Weg berechnet werden.
        Dabei wird eine Schätzfunktion verwendet, um das Verfahren zu optimieren, indem der Abstand zum Zielknoten berechnet wird.
        Als Schätzfunktion wird die Methode heuristik verwendet, welche die Manhattan-Distanz berechnet.
            
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
        F[start] = self.heuristisch(start, ziel)

        # offene und geschlossene Knoten werden in einem Set gespeichert
        geschlossene_knoten = set()
        # zu Beginn wird der Startknoten zu den offenen Knoten hinzugefügt
        offene_knoten = set([start])
        gekommen_von = {}

        # Solange noch ein Knoten offen ist:
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

            # Aktualisierung der Werte für die Knoten neben dem aktuellen Knoten
            for item in graph[aktueller_knoten]:
                nachbar_knoten, gewichtung = item[0]

                if nachbar_knoten in geschlossene_knoten:
                    # dieser Knoten wurde bereits ausgeschöpft
                    continue
                
                kandidatG = G[aktueller_knoten] + gewichtung

                # falls der Nachbarknoten noch nicht offen ist, 
                # wird er als offener gespeichert
                if nachbar_knoten not in offene_knoten:
                    offene_knoten.add(nachbar_knoten)
                
                elif kandidatG >= G[nachbar_knoten]:
                    # Wenn der G-Wert schlechter als der vorher gefundene ist
                    continue

                # G-Wert wird angepasst
                gekommen_von[nachbar_knoten] = aktueller_knoten
                G[nachbar_knoten] = kandidatG
                
                # Abstand zum Zielknoten wird geschätzt
                H = self.heuristisch(nachbar_knoten, ziel)
                F[nachbar_knoten] = G[nachbar_knoten] + H
        
        # Falls kein Weg gefunden wurde wird None zurückgegeben
        return None

    def heuristisch(self, knoten1, knoten2):
        """ Methode als heuristische Funktion im A*-Algorithmus
        
        Es wird die Manhattan-Distanz zwischen zwei Knoten berechnet.
        
        Args:
            knoten1: erster Knoten
            knoten2: zweiter Knoten
            
        Returns:
            float. Manhatten-Distanz zwischen den beiden Knoten
        """
        
        return self.manhattanDistanz(*knoten1, *knoten2)

    def dfs(self, graph, aktueller_knoten, alte_ladung, a_alte_ladung, aktuelle_ladung_batterien, pfad=[]):
        """
            TODO
        """

        pfad.append(aktueller_knoten)
        # print("Neuer Pfad: ", pfad)

        if len(pfad) > 2:
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
            # da der Roboter sich am Anfang bewegt und sozusagen keine Ersatzbatterie hinterlässt,
            # wird die Postion aus dem Dictionary gelöscht
            if len(pfad) == 2:
                del aktuelle_ladung_batterien[(self.roboter[0], self.roboter[1])]
                
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
        # TODO
        # Hier jetzt dann noch die Ladung leer machen
        if len(restliche_batterien) == 1 and aktueller_knoten == restliche_batterien[0]:
            print("YESSS")
            return pfad, aktuelle_ladung

        # für benachbarte Knoten wird die DFS aufgerufen
    
        # sortierte_liste_nachfolger = sorted(
        #     graph[aktueller_knoten], key=lambda item: item[0][1])
        
        # sortierte_liste_nachfolger = sorted(
            # graph[aktueller_knoten], key=lambda item: self.abwägung(*item[0][0], item[0][1], aktuelle_ladung_batterien), reverse=True
        # )
        
        
        sortierte_liste_nachfolger = sorted(graph[aktueller_knoten], key=lambda item: self.abwägung(*item[0][0], aktuelle_ladung_batterien), reverse=True)
        
        # sortierte_liste_nachfolger = graph[aktueller_knoten]

        for nachfolger_item in sortierte_liste_nachfolger:
            knoten, gewichtung = nachfolger_item[0]
            
            # falls der Knoten noch nicht besucht wurde
            if knoten in restliche_batterien:

                # Ladungsverbrauch wird abgezogen
                #aktuelle_ladung -= gewichtung

                return_item = self.dfs(graph=copy.deepcopy(graph), aktueller_knoten=knoten,
                                       alte_ladung=(
                    aktuelle_ladung-gewichtung),
                    a_alte_ladung=alte_ladung,
                    aktuelle_ladung_batterien=aktuelle_ladung_batterien.copy(),
                    pfad=pfad.copy())

                # print("Pfad: ", p)
                # return_item = (pfad, ladung)
                if return_item:
                    return return_item
                    # return p

            # # falls alle Batterien besucht wurden
            # elif not restliche_batterien:
            #     # return pfad
            #     #return pfad
            else:
                pass
                # return pfad
                # if len(restliche_batterien) == 1 and aktueller_knoten == restliche_batterien[0]:
                #     print("YESSS")
                #     return pfad


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

        # Damit das Tk-Fenster im Vordergrund ist und bleibt
        self.attributes('-topmost', True)
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
        time.sleep(0.5)
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
        self.__init__(self.size, self.roboter_start,
                      self.anzahl_batterien, self.batterien_start)
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
        (x_robo, y_robo, ladung_roboter), id_liste = list(
            self.roboter.items())[0]
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

        # if max([ladung[2] for ladung in self.batterien.keys()]) == 0 and ladung_roboter == 0:
        #     print("Max Ladung Batterien", max(
        #         [ladung[2] for ladung in self.batterien.keys()]))
        #     # höchste Ladung der Ersatzbatterien ist 0 und die Ladung des Roboters ist auf 0
        #     # Spiel fertig gelöst
        #     # reward += REWARD_FINISH
        #     done = True

        # Aktualisierung der Klassenvariable
        self.roboter[(x_robo, y_robo, ladung_roboter)] = id_liste
        # self._update_gui()

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
        print(
            f"\n>> Neuer State: {new_state} >> Reward: {reward} >> Fertig? {done}")
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

    eingabe2 = """ 
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

    eingabe3 = """
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

    eingabe4 = """
    100
    40,25,20
    0
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

    s = Steuerung(eingabe5)
