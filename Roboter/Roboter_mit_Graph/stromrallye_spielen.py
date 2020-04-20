#!/usr/bin/python

# 2. Runde Bundeswettbewerb Informatik 2019/20
# Aufgabe 1: Stromrallye (Spielen)
__author__ = "Christoph Waffler"
__version__ = 20200420

from random import * 

import sys
# Import von Tkinter
if sys.version_info.major == 2:
    import Tkinter as tk
    import Tkinter.scrolledtext as scrolledtext
    from Tkinter import messagebox
    from Tkinter import ttk
else:
    import tkinter as tk
    from tkinter import messagebox
    import tkinter.scrolledtext as scrolledtext
    from tkinter import ttk
    
import numpy as np
import time

class SpielErzeugen:
    def __init__(self, schwierigkeit: int, größe_spielfeld: int):
        """  Erstellen einer Spielsituation
        
        Schwierigkeit ist im Bereich von 1 bis 3:
            - 1 --> leicht
            - 2 --> mittel
            - 3 --> schwer
        
        Größen des Spielfelds
            - 10 --> 10 x 10
            - 12 --> 12 x 12
            - 14 --> 14 x 14

        """
        # Start der Zeitmessung
        self.start_zeit = time.time()
        
        # Klassenvariablen werden zugewiesen
        self.schwierigkeit = schwierigkeit
        self.size = größe_spielfeld
               
        
        # Zufallszahlen für die x- und y-Koordinate des Startpunktes
        # diese liegen im Bereich 1 bis Größe des Spielfelds
        x_start = randint(1, self.size)
        y_start = randint(1, self.size)
        
        startpunkt = [x_start, y_start]
        
        # Bereich der Schritte festlegen
        if self.schwierigkeit == 1:
            self.bereich_schritte = [3, 5]
        elif self.schwierigkeit == 2:
            self.bereich_schritte = [5, 10]
        elif self.schwierigkeit == 3:
            self.bereich_schritte = [10, 15]
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
        
        # aktueller Punkt wird auf den zufällig ausgewählten Startpunkt gesetzt
        aktueller_punkt = startpunkt.copy()
        
        # in gesamte_positionen werden alle nacheinander besuchten Felder gespeichert
        gesamte_positionen = [aktueller_punkt]
        
        # für jede Batterie:
        for a in range(self.anzahl_batterien):
            
            # x- und y-Koordinaten der bisher gespeicherten Batterien wird ermittelt
            batterien_x_y = list(map(
                lambda batterie: batterie[:2], self.batterien
            ))
            
            # Anzahl der Schritte wird zufällig bestimmt                     
            anzahl_schritte = randint(*self.bereich_schritte)
                                
            # besuchte Felder bevor eine neue Batterie 'gelegt' wird
            positionen = []
            
            # mithilfe von s wird die while-Schleife gesteuert
            s = anzahl_schritte
            while s >= 0:
                
                # falls alle Schritte gemacht wurden
                # und die Batterie im nächsten Schritt gelegt wird,
                # wird überprüft, ob dieses Feld nicht schon mal durch Schritte bereits besucht wurde
                # Ist dies der Fall so wird ein noch ein weiterer Schritt gemacht
                if s == 0:
                    if aktueller_punkt in gesamte_positionen or aktueller_punkt in positionen[:-1]:
                        s += 1
                        anzahl_schritte += 1
                    else:
                        # wenn nicht, dann wird s um 1 verringert und die Batterie anschließend gelegt
                        s -= 1
                    continue
            
                # eine neue Position (neues Feld) wird bestimmt
                neue_position = self.randomStep(*aktueller_punkt, batterien_x_y)
                
                # falls keine neue Position gefunden wurde,
                # wird noch mal 'zurückgegangen' und ein anderes Feld ausgewählt
                if neue_position == None:
                    anzahl_schritte += 1
                    s += 1
                else:
                    positionen.append(neue_position)
                    s -= 1
                
                
                # aktueller Punkt ist das letzte hinzugefügte Feld
                if positionen:
                    aktueller_punkt = positionen[-1]
                else:
                    # falls in positionen keine Felder besucht wurden, 
                    # wird das letzte Element von gesamte_positionen ausgewählt
                    aktueller_punkt = gesamte_positionen[-1]
                
            # Auf dem aktuellen Feld (aktueller Punkt) wird eine Batterie gelegt.
            # Die Ladung der Batterie ist die Anzahl der zurückgelegten Schritte
            self.batterien.append(
                (*aktueller_punkt, anzahl_schritte)
            )
            
            # die gesamte Liste der besuchten Felder wird erweitert
            gesamte_positionen.extend(positionen)
        
        # die besuchten Felder werden umgedreht,
        # da der Roboter 'von hinten' starten soll
        gesamte_positionen.reverse()
        self.gesamte_positionen = gesamte_positionen

        # Spielfeld wird graphisch erzeugt
        self.erzeugeUmgebung()
        
    def randomStep(self, x_akt: int, y_akt: int, vorhandene_batterien: list):
        """ Methode zum Auswählen eines zufälligen Nachbarfeldes, das besucht werden kann.
        
        Das zu besuchende Nachbarfeld sollte nicht durch eine Ersatzbatterie bereits belegt sein.
        
        Args:
            x_akt (int): x-Koordinate des Ausgangsfelds
            y_akt (int): y-Koordinate des Ausgangsfelds
            vorhandene_batterien (list): Liste mit den x- und y-Koordinaten der bisher erstellten Batterien

        Returns:
            tuple. Nachbarfeld, das frei ist und somit besucht werden kann        
        """
        
        # in schritte werden die möglichen Nachbarfelder hinzugefügt
        schritte = []
        aktuelle_position = [x_akt, y_akt]
        
        # Die Positionen der Felder unterhalb, oberhalb, rechts und links des Ausgangsfeld werden bestimmt
        # Diese werden als tuple gespeichert.
        
        unten = aktuelle_position.copy()
        unten[1] += 1
        unten = tuple(unten)
        if unten in vorhandene_batterien:
            unten = None
        
        oben = aktuelle_position.copy()
        oben[1] -= 1
        oben = tuple(oben)
        if oben in vorhandene_batterien:
            oben = None
        
        rechts = aktuelle_position.copy()
        rechts[0] += 1
        rechts = tuple(rechts)
        if rechts in vorhandene_batterien:
            rechts = None
        
        links = aktuelle_position.copy()
        links[0] -= 1    
        links = tuple(links)
        if links in vorhandene_batterien:
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
                    
            return zufallsschritt
        
        
        # falls nicht, wird None zurückgegeben
        else:
            return None
         
    def erzeugeUmgebung(self):
        """ Methode zur Erstellung der graphischen Benutzeroberfläche mithilfe der Klasse Environment """
        
        # der Startpunkt des Roboters ist die letzte Batterie 
        roboter = self.batterien.pop(-1)
        anzahl_batterien = len(self.batterien)

        self.ende_zeit = time.time()
        benötigte_zeit = self.ende_zeit - self.start_zeit
        print(f">> Laufzeit des Programms: {benötigte_zeit} Sekunden \n (Start der Zeitmessung bei Aufruf der main-Methode)\n\n")

        
        # Konsolenausgabe mit den Daten
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
        
        # Visualisierung wird erstellt 
        self.umgebung = Environment(self.size, roboter, len(self.batterien), self.batterien)
 
    def wegInAnweisungen(self, punkte: list):
        """ Methode zur Konvertierung von einzelnen Punkten in Schritte 
        
        Args:
            punkte (list): Liste mit Punkten, aus denen eine Abfolge von Schritten ermittelt werden soll.
            
        Returns:
            list. Abfolge von Schrittanweisungen für den Roboter, z.B. 0 --> Schritt nach oben        
        """     
        
        # in abfolge_schritte werden alle Schrittanweisungen gespeichert
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
  
    def zeigeLösung(self):    
        """ Methode zum Ausgeben der Lösung in der Konsole und Visualisierung der Schritte
            
        Diese Methode kann bei Bedarf vom Eingabefenster aufgerufen werden, wenn der Benutzer eine Lösung sehen möchte.
        """
         
        # Konvertierung der einzelnen besuchten Felder in Schrittanweisungen für den Roboter
        schrittanweisungen_roboter_lösung = self.wegInAnweisungen(self.gesamte_positionen)
        
        print(f"\n\n> Lösung: \n>> Alle besuchten Felder in richtiger Reihenfolge: \n > {self.gesamte_positionen}")
        
        # Abfolge der Schritte wird von Zahlen zu deutschen Wörtern 'konvertiert'
        abfolge_schritte_deutsch = []
        for schritt in schrittanweisungen_roboter_lösung:
            if schritt == 0:
                abfolge_schritte_deutsch.append('oben')
            elif schritt == 1:
                abfolge_schritte_deutsch.append('unten')
            elif schritt == 2:
                abfolge_schritte_deutsch.append('links')
            elif schritt == 3:
                abfolge_schritte_deutsch.append('rechts')
        
        print(f"\n>> Abfolge von {len(abfolge_schritte_deutsch)} Schritten für den Roboter in deutscher Sprache: \n > {abfolge_schritte_deutsch}")
        
        # Roboter wird mithilfe der Schrittanweisungen gesteuert
        for schritt in schrittanweisungen_roboter_lösung:
            self.umgebung.step(schritt)
            self.umgebung.update()
        
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
        
        
class EingabeFenster(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.spiel = None
        
        # Eingabefenster wird erstellt
        self.erstelleEingabeFenster()
    
    def erstelleEingabeFenster(self):
        # Label für Schwierigkeitsgrad
        self.label1 = tk.Label(self, text="Schwierigkeitsgrad auswählen:")
        self.label1.pack(side=tk.TOP)
        
        # Eine Combobox mit den Schwierigkeitsgraden wird erstellt
        self.schwierigkeitsgrade = {'Leicht': 1, 'Mittel': 2, 'Schwer': 3}
        self.auswahl_liste_schwierigkeitsgrad = ttk.Combobox(
            self,
            values=list(self.schwierigkeitsgrade.keys()),
            state='readonly'
        )
        self.auswahl_liste_schwierigkeitsgrad.pack(side=tk.TOP)
        
        # Label für die Größe des Spielfelds
        self.label2 = tk.Label(self, text="Größe des Spielfelds auswählen:")
        self.label2.pack(side=tk.TOP)
        
        # Eine Combobox mit den Größen des Spielfelds
        self.größen_spielfeld = {'10 x 10': 10, '12 x 12': 12, '14 x 14': 14}
        self.auswahl_liste_größe_spielfeld = ttk.Combobox(
            self,
            values=list(self.größen_spielfeld.keys()),
            state='readonly'
        )
        self.auswahl_liste_größe_spielfeld.pack(side=tk.TOP)
        
        # blauer Button für die Anzeige der Lösung
        self.button_lösung = tk.Button(
            self,
            width=10,
            height=3,
            text='Lösung anzeigen\n+ Roboter automatisch bewegen lassen',
            command=self.zeigeLösung)
        
        self.button_lösung['bg'] = '#52CDFB'
        self.button_lösung.pack(side=tk.BOTTOM, fill=tk.BOTH)
        
        
        # gelber Start-Button
        self.button_start = tk.Button(
            self,
            width=10,
            height=3,
            text="Erzeuge Spielumgebung",
            command=self.starte)
        
        self.button_start['bg'] = 'yellow'
        self.button_start.pack(side=tk.BOTTOM, fill=tk.BOTH)
       
    def starte(self):
        """ Start-Methode, die vom Start-Button aufgerufen wird. 
            
            Dabei wird eine neue Spielsituation mithilfe der Klasse SpielErzeugen erstellt. 
        """
        
        # boolescher Wert zum Überprüfen, ob das Eingabefenster vom Benutzer richtig bedient wurde
        korrekte_eingabe = True

        # Der bei der Combobox ausgewählte Schwierigkeitsgrad wird ermittelt.
        ausgewählter_grad = self.auswahl_liste_schwierigkeitsgrad.get()
        
        if ausgewählter_grad != "":
            schwierigkeitsgrad = self.schwierigkeitsgrade[ausgewählter_grad]
        
        else:  
            messagebox.showwarning("Fehler!", "Schwierigkeitsgrad angeben!")
            korrekte_eingabe=False              

        # Ebenfalls wird die ausgewählte Größe abgerufen.
        ausgewählte_größe = self.auswahl_liste_größe_spielfeld.get()
        
        if ausgewählte_größe != "":
            größe_spielfeld = self.größen_spielfeld[ausgewählte_größe]            
        
        else:
            messagebox.showwarning("Fehler!", "Größe des Spielfelds auswählen!")
            korrekte_eingabe=False


        # Falls eine korrekte Eingabe erfolgte, kann nun eine Spielsituation mit den ausgewählten Parametern erstellt werden.
        if korrekte_eingabe:            
            # Klasse SpielErzeugen wird aufgerufen
            self.spiel = SpielErzeugen(schwierigkeitsgrad, größe_spielfeld)
                
    def zeigeLösung(self):
        """ Methode zum Aufzeigen einer Lösung mithilfe der Methode zeigeLösung des Spiel-Objekts, 
            die die Spielsituation erstellt hat.
        """
        # falls schon ein Spiel erstellt wurde
        if self.spiel:
            self.spiel.zeigeLösung()
        
        # Fehlermeldung falls der Button zu früh betätigt wurde
        else:
            messagebox.showerror("Fehler!", "Spielsituation wurde noch nicht erzeugt!")
    
            
        
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Eingabefenster")
    root.geometry('400x200')
    EingabeFenster(root).pack(side="top", fill="both", expand=True)
    root.mainloop()


