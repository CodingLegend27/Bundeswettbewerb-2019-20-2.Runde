#!/usr/bin/python


# 2. Runde Bundeswettbewerb Informatik 2019/20
# Autor: Christoph Waffler
# Aufgabe 1: Stromrallye (Spielen)

from random import * 
import tkinter as tk
import numpy as np
import time

class SpielErzeugen:
    def __init__(self, schwierigkeit: int):
        """ Schwierigkeit ist im Bereich von 1 bis 3:
            - 1 --> leicht
            - 2 --> mittel
            - 3 --> schwer
        """
        self.schwierigkeit = schwierigkeit
        # Quadratisches Spielfeld mit 8 x 8 Feldern
        self.size = 8
               
        
        # Zufallszahlen für die x- und y-Koordinate des Startpunktes
        # diese liegen im Bereich 1 bis Größe des Spielfelds
        x_start = randint(1, self.size)
        y_start = randint(1, self.size)
        
        startpunkt = [x_start, y_start]
        
        # Bereich der Schritte festlegen
        if self.schwierigkeit == 1:
            self.max_bereich_schritte = [1, 5]
        elif self.schwierigkeit == 2:
            self.max_bereich_schritte = [5, 10]
        elif self.schwierigkeit == 3:
            self.max_bereich_schritte = [10, 15]
        else:
            raise ValueError
        
        # Anzahl Batterien festlegen (Anzahl Züge)
        if self.schwierigkeit == 1:
            self.anzahl_batterien = 5
        elif self.schwierigkeit == 2:
            self.anzahl_batterien = 10
        elif self.schwierigkeit == 3:
            self.anzahl_batterien = 15
        else:
            raise ValueError
        
        # Speicherung der Batterien
        self.batterien = []
        aktueller_punkt = startpunkt.copy()
        
        gesamten_schritte = []
        
        print(f">> Es werden {self.anzahl_batterien} Batterien erzeugt")
        for a in range(self.anzahl_batterien):
            
            batterien_x_y = list(map(
                lambda batterie: batterie[:2], self.batterien
            ))
                        
            anzahl_schritte = randint(*self.max_bereich_schritte)
                                
            positionen = []
            
            s = anzahl_schritte
            while s > 0:
                neue_position = self.randomStep(*aktueller_punkt, batterien_x_y)
                if neue_position == None:
                    print("naj")
                    positionen.pop()
                    s += 1
                else:
                    positionen.append(neue_position)
                    s -= 1
                
                if positionen:
                    aktueller_punkt = positionen[-1]
                else:
                    aktueller_punkt = gesamten_schritte[-1]
                
                
            
            self.batterien.append(
                (*aktueller_punkt, anzahl_schritte)
            )
            
            gesamten_schritte.extend(positionen)
            
            
            
            
        gesamten_schritte.reverse()
        # Konvertierung in Schrittanweisungen
        self.schrittanweisungen_roboter_lösung = self.wegInAnweisungen(gesamten_schritte)
        
        
        
        self.erzeugeUmgebung()
        
     
    
    def zufälligerSchritt(self, x_akt: int, y_akt: int, restliche_batterien_x_y: list):
        x_start, y_start = x_akt, y_akt
        """ zufälliger Schritt wird ausgewählt
        
        """
        # zufällige Schrittrichtung
        schritt = randint(0, 3)
        # 0: Schritt nach oben
        # 1: Schritt nach unten
        # 2: Schritt nach links
        # 3: Schritt nach rechts
        schritt_möglich = True
        if schritt == 0:
            
            if y_akt == 1: 
                schritt_möglich = False
            
            else:
                y_akt -= 1
            
        elif schritt == 1:
            
            if y_akt == self.size:
                schritt_möglich = False
                
            else:
                y_akt += 1
        
        elif schritt == 2:
            
            if x_akt == 1:
                schritt_möglich = False
            
            else:
                x_akt -= 1
        
        elif schritt == 3:
            
            if x_akt == self.size:
                schritt_möglich = False
                
            else:
                x_akt += 1
        
        if schritt_möglich:
            
            # falls die neuen Koordinaten und die alten Koordinaten identisch sind
            # oder auf den aktuellen Koordinaten sich bereits eine Batterie befindet
            # --> rekursiver Aufruf
            if x_akt == x_start and y_akt == y_start or (x_akt, y_akt) in restliche_batterien_x_y:
                return self.zufälligerSchritt(x_start, y_start, restliche_batterien_x_y)
            
            else:
                return x_akt, y_akt
        
        else:
            return self.zufälligerSchritt(x_start, y_start, restliche_batterien_x_y)


    def randomStep(self, x_akt: int, y_akt: int, restliche_batterien: list):
        schritte = []
        aktuelle_position = [x_akt, y_akt]
        
        # Die Positionen der Felder unterhalb, oberhalb, rechts und links des Ausgangsfeld werden bestimmt
        unten = aktuelle_position.copy()
        unten[1] += 1
        unten = tuple(unten)
        if unten in restliche_batterien:
            unten = None
        
        oben = aktuelle_position.copy()
        oben[1] -= 1
        oben = tuple(oben)
        if oben in restliche_batterien:
            oben = None
        
        rechts = aktuelle_position.copy()
        rechts[0] += 1
        rechts = tuple(rechts)
        if rechts in restliche_batterien:
            rechts = None
        
        links = aktuelle_position.copy()
        links[0] -= 1    
        links = tuple(links)
        if links in restliche_batterien:
            links = None    
        
        # Je nach Lage der aktuellen Position werden die Nachbarfelder zu den möglichen Schritten hinzugefügt
        if y_akt > 1:            
            schritte.append(oben)
        
        if y_akt < self.size:
            schritte.append(unten)
        
        if x_akt > 1:
            schritte.append(links)
        
        if x_akt < self.size:
            schritte.append(rechts)
        
        # Alle 'None' werden entfernt
        [schritte.remove(None) for i in range(schritte.count(None))]
        
        
        # falls mögliche Nachbarfeld gefunden wurden
        # und somit ein Schritt möglich ist
        if schritte:
            # auszuwählender Bereich wird bestimmt            
            bereich = len(schritte)-1
            
            # ein zufälliger Index im Bereich wird ausgewählt
            zufalls_index = randint(0, bereich)
            
            # über den Index wird das zufällige Nachbarfeld ausgewählt
            # und somit der Zufallsschritt bestimmt
            zufallsschritt = schritte[zufalls_index]
            
            print("neuer Zufallsschritt", zufallsschritt)

            
            return zufallsschritt
        
        
        # falls nicht, wird None zurückgegeben
        else:
            print("None wird zurückgegeben")
            return None
   
    def wegInAnweisungen(self, punkte: list):
        """ konvertierung von einzelnen Punkten in Schritte """     
        abfolge_schritte = []
        
        for index in range(len(punkte)):
            if index > 0:
                # Teilweg aus den Punkten P1 und P2
                p1 = punkte[index-1]
                p2 = punkte[index]
               
                # die Differenzen der x- und y-Koordinaten wird berechnet
                delta_x = p2[0] - p1[0]
                delta_y = p2[1] - p1[1]
               
                # je nach Differenz muss eine bestimmte Bewegung ausgeführt werden,
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
        
                abfolge_schritte.append(bewegung)
        
        return abfolge_schritte
            
        



        
        
        
    def erzeugeUmgebung(self):
        """
        """
        # der Startpunkt des Roboters ist die letzte Batterie 
        roboter = self.batterien.pop(-1)
        anzahl_batterien = len(self.batterien)

        print(f">> Spielgröße: {self.size}")
        print(f">> Startposition des Roboters {roboter}")
        print(f">> Anzahl der Batterien: {anzahl_batterien}")
        print(f">> Koordinaten der Batterien: {self.batterien}")
        
        # Ausgabe im BwInf-Format
        print(f"\n >> Ausgabe im BwInf-Format: \n{self.size}")
        print(f"{roboter[0]},{roboter[1]},{roboter[2]}")
        print(f"{anzahl_batterien}")
        for batterie in self.batterien:
            print(f"{batterie[0]},{batterie[1]},{batterie[2]}")
        
           
        umgebung = Environment(self.size, roboter, len(self.batterien), self.batterien)
        umgebung._build_stromrallye()
        
        # for schritt in self.schrittanweisungen_roboter_lösung:
        #     umgebung.step(schritt)
        #     umgebung.update()
        
        tk.mainloop()


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
    
    spiel = SpielErzeugen(2)
        
        
        
        
