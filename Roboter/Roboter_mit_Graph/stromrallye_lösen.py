#!/usr/bin/python

# 2. Runde Bundeswettbewerb Informatik 2019/20
# Aufgabe 1: Stromrallye (Lösen)
__author__ = "Christoph Waffler"
__version__ = 20200420

from collections import defaultdict
import copy
import numpy as np
import time

import sys
import random
# Import von Tkinter
if sys.version_info.major == 2:
    import Tkinter as tk
    import Tkinter.scrolledtext as scrolledtext
    from Tkinter import messagebox
else:
    import tkinter as tk
    from tkinter import messagebox
    import tkinter.scrolledtext as scrolledtext

import math

class Berechnungen:
    def __init__(self, eingabe: list):
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
            tuple. Tuple mit der x-, y-Koordinate und der Ladung, die als int dargestellt werden.   
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


    def main(self):
        """ Hauptmethode des gesamten Programms
        """
        
        # Start der Zeitmessung
        start_zeit = time.time()
        
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
        return_item = self.dfs(
            graph=self.graph,
            aktueller_knoten=self.roboter[:2],
            alte_ladung=0,
            a_alte_ladung=0, 
            aktuelle_ladung_batterien=aktuelle_ladung_batterien)
        
        # falls kein Pfad gefunden wurde:
        if not return_item:
            
            # Hier wird auch die Laufzeit ermittelt
            ende_zeit = time.time()
            
            print(">> Die eingegebene Spielsituation ist nicht lösbar! \nKein Pfad wurde gefunden!")
            
            print(f"\n>> Laufzeit des Programms: {ende_zeit-start_zeit} Sekunden \n (Start der Zeitmessung bei Aufruf der main-Methode)")
            
            messagebox.showerror("Fehler", "Kein Pfad gefunden!")
            return

        pfad, restliche_ladung = return_item
        
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
            
            # eine Liste mit Nachbarpunkten von der letzten Position ausgehend wird erstellt
            liste_nachbarn1 = self.findeFreieNachbarpunkte(*letzte_position, batterien_x_y)

            # Prüfen, ob ein Tuple in der Liste ist
            if any(isinstance(item, tuple) for item in liste_nachbarn1):
                
                # Liste wird so sortiert, dass eine Zahl am Anfang ist, welche ausgewählt wird
                liste_nachbarn1.sort(key=lambda x: (x is None, x))
                # dies ist der erste Nachbar
                erster_nachbar = liste_nachbarn1[0]
                
                # eine Liste mit freien Nachbarpunkten vom ersten Nachbarn ausgehend wird erstellt
                liste_nachbarn2 = self.findeFreieNachbarpunkte(*erster_nachbar, batterien_x_y)
                
                # Prüfen, ob eine Tuple in der Liste ist
                if any(isinstance(item, tuple) for item in liste_nachbarn2):
                    
                    # Liste wird so sortiert, dass eine Zahl am Anfang ist, welche ausgewählt wird
                    liste_nachbarn2.sort(key=lambda x: (x is None, x))
                    # dies ist der erste Nachbar
                    zweiter_nachbar = liste_nachbarn2[0]

                    # Schritt von letzter Position zum ersten Nachbarn
                    von_letzter_pos_zu_nachbar1 = self.findeWeg(*letzte_position, *erster_nachbar)[0]

                    # Schritt vom ersten Nachbarn zum zweiten Nachbarn
                    von_nachbar1_zu_nachbar2 = self.findeWeg(*erster_nachbar, *zweiter_nachbar)[0]

                    # Schritt vom zweiten Nachbarn zurück zum ersten
                    von_nachbar2_zu_nachbar1 = self.findeWeg(*zweiter_nachbar, *erster_nachbar)[0]

                    # es wird von der letzten Position zum ersten Nachbarn gegangen
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


        if restliche_ladung == 1:

            # Wenn am oberen Rand (also y-Koordinate gleich 1)
            # Schritt nach unten
            if letzte_position[1] == 1:
                abfolge_schritte.append(1)

            # sonst Schritt nach oben
            else:
                abfolge_schritte.append(0)
        
        # Abfolge der Schritte wird von Zahlen zu deutschen Wörtern 'konvertiert'
        abfolge_schritte_deutsch = []
        for schritt in abfolge_schritte:
            if schritt == 0:
                abfolge_schritte_deutsch.append('oben')
            elif schritt == 1:
                abfolge_schritte_deutsch.append('unten')
            elif schritt == 2:
                abfolge_schritte_deutsch.append('links')
            elif schritt == 3:
                abfolge_schritte_deutsch.append('rechts')
                
        ende_zeit = time.time()
                        
        print(f"\n>> Abfolge von {len(abfolge_schritte_deutsch)} Schritten für den Roboter in deutscher Sprache: \n > {abfolge_schritte_deutsch}")
        
        print(f"\n>> Laufzeit des Programms: {ende_zeit-start_zeit} Sekunden \n (Start der Zeitmessung bei Aufruf der main-Methode)")
        
        # Umgebung wird erstellt
        env = Environment(self.size, self.roboter,
                            self.anzahl_batterien, self.batterien)
        
        env._update_gui()
        # für jeden Schritt wird die Umgebung aufgerufen
        for schritt in abfolge_schritte:
            env.step(schritt)
            env.update()
   
   
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

                nachbarn = self.findeFreieNachbarpunkte(*aktuelle_position, batterien_x_y)

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

            return abfolge_schritten
        else:
            return None

    def findeFreieNachbarpunkte(self, x_akt, y_akt, potenzielle_hindernisse):
        """ Methode zum Ermitteln freier Nachbarpunkte.
        
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

            # aktuelle Position nicht am ganz oberen Rand
            if y_akt > 1:
                nachbarn.append(oben)
            
            # aktuell nicht ganz unten am Rand
            if y_akt < self.size:
                nachbarn.append(unten)
            
            # aktuell nicht ganz links am Rand         
            if x_akt > 1:
                nachbarn.append(links)
            
            # nicht ganz rechts am Rand
            if x_akt < self.size:
                nachbarn.append(rechts)            

            return nachbarn


    def astar(self, start, ziel, graph):
        """ A*-Algorithmus zur Berechnung des kürzesten Weg.
        
        Im gegebenen Graph soll vom Start- zum Zielknoten der kürzeste Weg berechnet werden.
        Dabei wird eine Schätzfunktion verwendet, um das Verfahren zu optimieren, indem der Abstand zum Zielknoten berechnet wird.
        Als Schätzfunktion wird die Methode heuristik_astar verwendet, welche die Manhattan-Distanz berechnet.
            
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
        
        Es wird die Manhattan-Distanz zwischen zwei Knoten berechnet.
        
        Args:
            knoten1: erster Knoten
            knoten2: zweiter Knoten
            
        Returns:
            float. Manhatten-Distanz zwischen den beiden Knoten
        """

        return self.manhattanDistanz(*knoten1, *knoten2)


    def dfs(self, graph, aktueller_knoten, alte_ladung, a_alte_ladung, aktuelle_ladung_batterien, pfad=[]):
        """ Methode zur rekursiven Tiefensuche im gegebenen Graphen        
        
        Args:
            graph (Graph): Graph als Datenstruktur zum Speichern der aktuellen Kantenbeziehungen der Ersatzbatterien
            aktueller_knoten (tuple): aktuell ausgewählter Knoten, der zum Pfad hinzugefügt wird
            alte_ladung (int): Ladung des vorherigen Knotens, die als a_alte_ladung im nächsten Schritt weitergegeben wird
            a_alte_ladung (int): veränderte Ladung der vorvorherig besuchten Batterie, dessen Ladung nun aktualisiert wird
            aktuelle_ladung_batterien (dict): Dictionary zum Speichern der aktuellen Ladungen der Batterien
            pfad (list): Liste zum Speichern der besuchten Batterien (Knoten des Graphen)
            
        Returns:
            list. Pfad mit einem Weg, den der Roboter zurücklegen muss, damit alle Batterien leer sind          
        """
        # aktueller Knoten wird zum Pfad hinzugefügt
        pfad.append(aktueller_knoten)
        #print(f"> Pfad: {pfad}")
        
        # ist der Pfad länger als 2 Elemente, so wird immer die Ladung des Vorvorgängers aktualisiert
        if len(pfad) > 2:
            
            # die Ladung des vorvorletzten Elements muss aktualisiert werden
            alter_knoten = pfad[-2]
            
            # bisherige Ladung des alten Knotens wird ermittelt
            bisherige_ladung = aktuelle_ladung_batterien[alter_knoten]
            
            # nur wenn die 'neue' (a_alte_ladung) des alten Knotens sich von der bisherigen Ladung unterscheidet,
            # ändern sich auch die erreichbaren anderen Ersatzbatterien von der aktuellen Position ausgehend
            # und somit auch die Nachbarknoten im Graphen
            if a_alte_ladung != bisherige_ladung:
                                
                # Aktualisierung des Dictionary zum Speichern der aktuellen Ladungen
                # die Ladung des vorvorletzten Elements wird auf a_alte_ladung gesetzt
                aktuelle_ladung_batterien[alter_knoten] = a_alte_ladung

                # restliche Batterien werden ermittelt
                restliche_batterien = self.filterListeBatterien(aktuelle_ladung_batterien)

                # aufgrund der veränderten Ladung des Vorvorgängers werden nun seine erreichbaren Batterien neu ermittelt
                erreichbare_batterien_neu = self.erreichbareBatterien(*alter_knoten, a_alte_ladung, restliche_batterien)
                
                # die Manhattan-Distanz wird berechnet und mithilfe der map()-Funktion als tuple mit der jeweiligen erreichbaren Batterie gespeichert
                erreichbare_batterien_neu = list(map(
                    lambda batterie: (*batterie, self.manhattanDistanz(*batterie, *alter_knoten)), 
                    erreichbare_batterien_neu
                ))
                
                # die Nachbarknoten der Vorvorgängers werden im Graphen aktualisiert
                graph.aktualisiereNachfolger(alter_knoten, erreichbare_batterien_neu)
                
            else:
                # restliche Batterien werden ermittelt
                restliche_batterien = self.filterListeBatterien(aktuelle_ladung_batterien)

        else:
            # Da der Roboter sich am Anfang bewegt und sozusagen keine Ersatzbatterie 'hinterlässt',
            # wird die Postion aus dem Dictionary gelöscht,
            # Auf dem Startfeld des Roboters befindet sich nun keine Batterie mehr.
            if len(pfad) == 2:
                del aktuelle_ladung_batterien[(self.roboter[0], self.roboter[1])]
                
            # restliche Batterien werden ermittelt
            restliche_batterien = self.filterListeBatterien(aktuelle_ladung_batterien)


        # die akutelle Ladung des aktuellen Knotens wird ausgelesen
        aktuelle_ladung = aktuelle_ladung_batterien[aktueller_knoten]
        
        
        # Falls nur noch eine Batterie übrig ist (die Batterie des aktuellen Knoten),
        # so ist die suche beendet.
        # Der Pfad und die aktuelle Ladung des aktuellen Knotens werden zurückgegeben
        if len(restliche_batterien) == 1 and aktueller_knoten == restliche_batterien[0] and alte_ladung == 0:
            return pfad, aktuelle_ladung

        
        # Heuristik
        # Mithilfe der Methode heuristik_dfs() wird für jeden Nachbarknoten der jeweilige Wert bestimmt.
        # Anhand dieses Werts wird die Liste absteigend sortiert,
        # dass der Nachbarknoten mit dem höchsten Wert an erster Stelle steht.
        # Somit wird die Tiefensuche beschleunigt.
        sortierte_liste_nachfolger = sorted(graph[aktueller_knoten], 
                                            key=lambda item: self.heuristik_dfs(*item[0][0], aktuelle_ladung_batterien, graph), reverse=True)
        
        # sortierte_liste_nachfolger = sorted(graph[aktueller_knoten], 
        #                                     key=lambda item: len(self.erreichbareBatterien(*item[0][0], item[0][1], restliche_batterien)), reverse=True)
        
        # für jeden Kindernknoten wird die Schleife aufgerufen
        for nachfolger_item in sortierte_liste_nachfolger:
            knoten, gewichtung = nachfolger_item[0]
            
            # falls der Knoten noch nicht besucht wurde
            if knoten in restliche_batterien:
                
                # Die Methode dfs wird nun rekursiv aufgerufen.
                
                # Dabei wird der Graph mithilfe des Moduls copy tiefenkopiert, 
                # da sonst eine Veränderung des Graphen in einem Nachbarknoten, die anderen auch beeinflussen würde.
                
                # Der Nachbarknoten ist dann der aktuelle_knoten.
                # Die alte Ladung des vorherigen Knoten ist die Differenz zwischen dessen ursprüngliche Ladung und die Gewichtung zum Nachbarknoten.
                # a_alte_ladung wird mit dem Wert von alte_ladung aufgerufen, und 'rückt somit eins weiter nach hinten'.
                
                # Das Dictionary zum Speichern der aktuellen Ladungen wird ebenfalls kopiert,
                # da sonst dieselben Probleme beim rekursiven Aufruf auftreten würden (wie bei graph).
                return_item = self.dfs(graph=copy.deepcopy(graph), aktueller_knoten=knoten,
                                        alte_ladung=(
                    aktuelle_ladung-gewichtung),
                    a_alte_ladung=alte_ladung,
                    aktuelle_ladung_batterien=aktuelle_ladung_batterien.copy(),
                    pfad=pfad.copy())

                # falls der rekursive Aufrufe ein Tuple zurückgibt,
                # wird dieses auch zurückgegeben
                if return_item:
                    return return_item

                # 'else:' Falls nichts zurückgegeben wird, geht dieser Teilzweig ins Leere und wird nicht weiter beachtet.


    def filterListeBatterien(self, aktuelle_ladung_batterien: dict):
        """ Als Liste der restlichen Batterien werden nur die x- und y-Koordinaten aller Batterien benötigt,
            die aktuell eine Ladung > 0 besitzten
            
            Args:
                aktuelle_ladung_batterien: Dictionary mit den aktuellen Ladungen der Batterien
                
            Returns:
                list. Eine Liste mit den x- und y-Koordinaten der Batterien, die eine Ladung > 0 besitzen.
        """
        # 1. Filtern der Batterien mit Ladung > 0
        restliche_batterien = list(filter(
            lambda batterie: batterie[1] > 0, list(
                aktuelle_ladung_batterien.items())
        ))
        # 2. Nur die x- und y-Koordinaten werden benötigt
        restliche_batterien = list(
            map(lambda batterie: batterie[0], restliche_batterien))

        return restliche_batterien
        
    def heuristik_dfs(self, x: int, y: int, batterien_aktuelle_ladung: dict, graph):
        """ Diese Methode dient als Optimierung der Tiefensuche (depth-first-search, DFS).

        Diese Methode liefert einen Wert, der die Auswahl zwischen den Nachbarknoten eines Knoten eines Graphen optimieren soll.

        Dabei wird der Wert zwischen den Nachbarknoten verglichen 
        und die Suche wird mit dem Nachbarknoten mit dem maximialen Wert fortgesetzt.

        Der Wert wird von zwei Faktoren beeinflusst: 
            - Ladung der Batterie (des aktuellen Nachbarknoten)
            - Abstand zum Startpunkt des Roboters

        Die Ladung der aktuellen Batterie (=Nachbarknoten) wird mithilfe des gegebenen Dictionary ermittelt.

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
        return aktuelle_ladung_batterie**2 * abstand
        
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
 
class Graph:
    """ gerichteter Graph zum Verwalten von Knoten und Kanten mit Gewichtungen """

    def __init__(self):
        """ Ein leeres Dictionary zum Speichern des Graphen wird erstellt.        
            Der Graph wird in Form einer Adjazenzliste gespeichert.        
        """
        self.adjazenzliste = defaultdict(list)

    def add_Kante(self, start: tuple, ende: tuple, gewichtung):
        """ Methode zum Hinzufügen einer neuen Kante.
        Die Kante besteht aus dem gegebenen Start- und Endknoten mit der gegebenen Gewichtung.
        
        Für diese Aufgabe wird ein gerichteter Graph benötigt, 
        daher muss die Kante nur einmal für den Startknoten hinzugefügt werden.
        
        Args:
            start (tuple): Startknoten
            ende (tuple): Endknoten
            gewichtung: Gewichtung der Kante
        """
        self.adjazenzliste[start].append({
            ende: gewichtung
        })

    def delete_Kante(self, start, entfernendes_item):
        """ Methode zum Entfernen eines Items aus dem gegebenen Startknoten.
        Das Item wird aus der Liste der Nachfolger-Elemente des Startknotens entfernt.
        
        Args:
            start (tuple): Startknoten
            entfernendes_item (dict): zu entfernendes Dictionary        
        """        
        self.adjazenzliste[start].remove(entfernendes_item)

    def __getitem__(self, key):
        """ Zurückgeben der Nachfolgeknoten zusammen mit deren Gewichtungen
        Args:
            key (tuple): Startknoten
        
        Returns:
            list. Liste mit Nachfolgeknoten
        """
        return [list(n.items()) for n in self.adjazenzliste[key]]

    def aktualisiereNachfolger(self, knoten, neue_nachfolger: list):
        """ Methode zur Aktualisierung der Nachfolgerknoten des gegebenen Knotens.
        
        Dabei werden neue Nachfolger hinzugefügt, nicht mehr vorhandene werden entfernt.
        
        Args:
            knoten (tuple): zu aktualisierender Knoten
            neueNachfolger (list): Liste mit neuen Nachfolgern zusammen mit deren Gewichtung für die Kante
        """
        
        # hier muss .copy() verwendet werden, 
        # da sonst sich die Liste ursprüngliche_nachfolger_items bei Entfernen von Knoten aus der Adjazenzliste verändert!
        ursprüngliche_nachfolger_items = self.adjazenzliste[knoten].copy()
        for nachfolger_item in neue_nachfolger:

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

class EingabeFenster(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.erstelleEingabeFenster()

    def erstelleEingabeFenster(self):

        # Eingabefeld
        self.textfeld = scrolledtext.ScrolledText(self, width=40, height=10)
        self.textfeld.insert(tk.END, "Spielsituation bitte hier im Format des BwInf einfügen:")
        self.textfeld.pack(side=tk.TOP)
        
        # Button zum Starten
        self.button_start = tk.Button(
            self,
            width=10,
            height=3,
            text="Starte Berechnungen",
            command=self.starte)
        # Gelber Button
        self.button_start['bg'] = 'yellow'
        self.button_start.pack(side=tk.BOTTOM, fill=tk.BOTH)
         
    def starte(self):
        # die Eingabe des Nutzers wird aus dem Textfenster gelesen
        eingabe = self.textfeld.get('1.0', 'end').split()

        # Eingabefenster wird geschlossen
        self.destroy()
        
        # Ruft die Klasse berechnungen auf, welche den Pfad berechnet,
        # den der Roboter zurücklegen muss, damit alle Batterien leer sind                
        b = Berechnungen(eingabe)

class Environment(tk.Tk, object):

    def __init__(self, size: int, roboter: tuple, anzahl_batterien: int, batterien: list):
        """ erstellt eine Umgebung mit der gegebenen Eingabe """
        super(Environment, self).__init__()
        

        self.size = size
        self.UNIT = 40
        self.title('Stromrallye')
        self.geometry('{0}x{1}'.format(800, 800))

        # Damit das Tk-Fenster im Vordergrund ist und bleibt
        self.attributes('-topmost', True)
        # Ausgangszustand wird gespeichert, damit die Umgebung wieder zurückgesetzt werden kann
        self.roboter_start = roboter
        self.batterien_start = batterien

        self.origin = np.array([self.UNIT/2, self.UNIT/2])


        # Batterien:
        self.anzahl_batterien = anzahl_batterien
        # die Batterien werden gesammelt in einem Dictionary ebenfalls wie der Roboter in der Form:
        # (x, y, ladung) gespeichert
        # wobei (x, y, ladung) als Key des Dictionary fungiert und die id des Text-Widgets von Tkinter der jeweilige Value ist
        # der Value wird später erstellt
        self.batterien = dict.fromkeys(batterien)

        # Die Position des Roboters oder der Batterien werden in einem Dictionary mit der Form (x, y, ladung) gespeichert
        # Key ist (x, y, ladung) und der Value ist eine Liste mit der ID des grünen Quadrats (stellt den Roboter da) und mit der ID des Text-Widgets
        self.roboter = dict.fromkeys([roboter])
        

        
        self.frame = tk.Frame(self, width=800, height=800)
        self.frame.pack(expand=True, fill=tk.BOTH)
        
        # Stromrallye mit den Batterien und Roboter wird erstellt
        self._build_stromrallye()

    def _build_stromrallye(self):
        """ in dieser Methode wird das Spielbrett auf Ausgangsstellung auf einer Zeichenfläche (Canvas) gezeichnet """

        # Canvas objekt wird erstellt
        # weißer Hintergrund mit gegebener, quadratischer Größe des Spielbretts
        self.canvas = tk.Canvas(
            self.frame, bg='white',
            height=800,
            width=800)

        # Gitter erstellen
        for spalte in range(0, self.size * self.UNIT, self.UNIT):
            x0, y0, x1, y1 = spalte, 0, spalte, self.size * self.UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for reihe in range(0, self.size * self.UNIT, self.UNIT):
            x0, y0, x1, y1 = 0, reihe, self.size * self.UNIT, reihe
            self.canvas.create_line(x0, y0, x1, y1)

        # Ersatzbatterien mit aktuellem Akkustand zeichnen
        for key in self.batterien.keys():
            x, y, ladung = key

            # Mittelpunkt des Feldes der jeweiligen Ersatzbatterie
            batt_center = np.array([(x-1) * self.UNIT, (y-1) * self.UNIT]) + self.origin

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
        robo_center = np.array([(x-1) * self.UNIT, (y-1) * self.UNIT]) + self.origin

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


        # Horizontale und vertikale Scrollbar wird hinzugefügt
        self.scrollbar_horizontal = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.scrollbar_vertical = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)
    
        # Konfiguration der Scrollbar
        self.scrollbar_horizontal.config(command=self.canvas.xview)       
        self.scrollbar_vertical.config(command=self.canvas.yview)
        
        # Konfiguration des Canvas
        self.canvas.config(xscrollcommand=self.scrollbar_horizontal.set, yscrollcommand=self.scrollbar_vertical.set, scrollregion=(0,0,self.size*self.UNIT,self.size*self.UNIT))
                
        # Canvas wird entpackt
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.focus()

    def _update_gui(self):
        """ aktualisiert die angezeigten Zahlen und die Position des Roboters auf dem GUI --> Rendering der Oberfläche"""
        
        # gibt an wie lange die Zeit zwischen den einzelnen Schritten des Roboters ist
        time.sleep(0.5)
        
        # Roboter aktualisieren:
        # grünes Quadrat bewegen und die Zahl für die Ladung der Bordbatterie aktualisieren
        (x, y, ladung), [id_quadrat, id_text] = list(self.roboter.items())[0]
        # x- und y-Koordinate der alten Position
        old_coords = np.array(self.canvas.coords(id_quadrat)[0:2])
        new_coords = np.array([(x-1) * self.UNIT+5, (y-1) * self.UNIT+5])
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
        
        # Canvas wird entpackt
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
        """ bewegt den Roboter in der Umgebung, wobei gilt:
            nach oben: 0
            nach unten: 1
            nach links: 2
            nach rechts: 3
        """
        # speichert den auszuführenden Vorgang
        
        # Mithilfe des booleschen Wert against_wall wird überprüft, 
        # ob der Roboter gegen eine Wand laufen würde.        
        # Ist das der Fall, so geht er nicht weiter und keine Ladung wird abgezogen
        # --> dadurch entsteht eine Überprüfung des Programms
        against_wall = False
        
        (x_robo, y_robo, ladung_roboter), id_liste = list(
            self.roboter.items())[0]
        self.roboter.pop((x_robo, y_robo, ladung_roboter))

        # Koordinate des Roboters wird je nach Schrittrichtung angepasst
        
        # ist er an der Wand,
        # so kommt an der gegenüberliegende Seite heraus
        
        # Schritt nach oben
        if action == 0:
            if y_robo > 1:
                # hoch: y-Koordinate -1
                y_robo -= 1
            else:
                against_wall = True            
                                
        # Schritt nach unten
        elif action == 1:
            if y_robo < self.size:
                # runter: y-Koordinate +1
                y_robo += 1
            else:
                against_wall = True

        # Schritt nach links
        elif action == 2:
            if x_robo > 1:
                # links: x-Koordinate -1
                x_robo -= 1
            else:
                against_wall = True

        # Schritt nach rechts
        elif action == 3:
            if x_robo < self.size:
                # rechts: x-Koordinate +1
                x_robo += 1
            else:
                against_wall = True

        if ladung_roboter > 0:
            if against_wall:
                # Schritt ist möglich
                print(">> Ein Schritt gegen die Wand wurde betätigt!")

        # Ladung der Bordbatterie -1
        ladung_roboter -= 1
        
        # Aktualisierung der Klassenvariable
        self.roboter[(x_robo, y_robo, ladung_roboter)] = id_liste

        # Überprüfung, ob sich der Roboter jetzt auf einem Feld mit einer Ersatzbatterie befindet
        for koordinaten, ladung_batterie in zip([koordinaten[0:2] for koordinaten in self.batterien.keys()], [ladung[2] for ladung in self.batterien.keys()]):
            if (x_robo, y_robo) == koordinaten:
                self.batterien[(x_robo, y_robo, ladung_roboter)] = self.batterien.pop((x_robo, y_robo, ladung_batterie))
                
                self.roboter[(x_robo, y_robo, ladung_batterie)] = self.roboter.pop((x_robo, y_robo, ladung_roboter))

        self._update_gui()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Eingabefenster")
    root.geometry('400x200')
    EingabeFenster(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
