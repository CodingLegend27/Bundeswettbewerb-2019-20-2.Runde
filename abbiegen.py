# 2. Runde Bundeswettbewerb Informatik 2019/20
# from PySide2.QtCore import Qt
# from PySide2.QtWidgets import *
from tkinter import *
import math

class Punkt():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self = (x, y)
   
    def __str__(self):
        """ Ausgabe der Koordinaten eines Punktes """
        return f"({self.x}/{self.y})"
 
    
class Kante():
    def __init__(self, startpunkt: Punkt, zielpunkt: Punkt):
        self.startpunkt = startpunkt
        self.zielpunkt = zielpunkt
        
        # Länge/Distanz der Kante wird als Gewichtung gespeichert
        self.gewichtung = berechneLänge(startpunkt, zielpunkt)
        
        self = (startpunkt, zielpunkt)
        
    def __iter__(self):
        """ implementierung der __iter__ - Methode, damit die Objekte von Kante iterierbar sind"""
        return iter((self.startpunkt, self.zielpunkt))
    
    def __str__(self):
        print("Hello \n\n")
        return f"Startpunkt: {startpunkt}; Zielpunkt: {zielpunkt}\n"
    
     
def berechneLänge(p1: Punkt, p2: Punkt):
    return math.sqrt(
        (p1.x - p2.x)**2
        + 
        (p1.y - p2.y)**2
    )


class EingabeFenster(Frame):
   
    def __init__(self, parent, *args, **kwargs):                
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

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
        eingabe = self.textfeld.get('1.0', 'end').rsplit()
        print(eingabe)
        
        # Zuweisung der Klassenvariablen durch die eingegebenen Daten
        anzahl_straßen = int(eingabe.pop(0))
        startpunkt = self.zuPunkt(eingabe.pop(0))
        zielpunkt = self.zuPunkt(eingabe.pop(0))
        liste_verbindungen = []
        for verbindung in range(int(len(eingabe)/2)):
             p1 = self.zuPunkt(eingabe.pop(0))
             p2 = self.zuPunkt(eingabe.pop(0))
             kante = Kante(p1, p2)
             liste_verbindungen.append(kante)
        
        print("\nAnzahl der Straßen: ", anzahl_straßen)
        print("Startpunkt: ", startpunkt)
        print("Zielpunkt: ", zielpunkt)
        print("Liste Verbindungen ", liste_verbindungen)      
        
        # Eingabefenster wird geschlossen
        self.destroy()
                
        # Zeichenfenster wird erstellt
        # TODO: Zeichenfenster
        e = ZeichenFenster(root, width=700, height=700)
        e.pack(side="top", fill="both", expand=True)
        e.zeichne(
            startpunkt=self.startpunkt,
            zielpunkt=self.zielpunkt,
            liste_verbindungen=self.liste_verbindungen
        )    
        
    
    def zuPunkt(self, eingabe) -> Punkt: 
        """ verwertet die Eingabe zu einem Objekt der Klasse Punkt aufgebaut ist
        z.B.: '('0','0')' """
        x = int(list(eingabe)[1]),
        y = int(list(eingabe)[3])
        return Punkt(x, y)
     
class Berechnungen():
    def __init__(self, anzahl_straßen: int, startpunkt: Punkt, zielpunkt: Punkt, liste_verbindungen: list):
        # Daten
        self.anzahl_straßen = anzahl_straßen
        self.startpunkt = startpunkt
        self.zielpunkt = zielpunkt
        self.liste_verbindungen = liste_verbindungen
     
    def berechneSteigungKante(kante: Kante):
        """ berechnet die Steigung der eingegebenen Kante """
        y_diff = kante.startpunkt.y - kante.zielpunkt.y
        x_diff = kante.startpunkt.x - kante.zielpunkt.x
        steigung = y_diff / x_diff
        return steigung

class Graph():
    def __init__(self):
        """ initialisiert einen Graph """
        self.__graph_dict = {}
        
    def Knoten(self):
        """ gibt die Knoten des Graphen wieder"""
        return list(self.__graph_dict.keys())
    
    def Kanten(self):
        """ gibt die Kanten des Graphen wieder"""
        return self.__generiereKanten()
    
    def addKnoten(self, knoten: Punkt):
        """ fügt die eingebenen Punkt als Kante zum Graphen
            brauch ich wahrscheinlich eh nicht xD
        """
        if knoten not in self.__graph_dict:
            self.___graph_dict[knoten] = []
        
    
    def addKante(self, kante: Kante):
        """ fügt die eingebene Kante zum Graph"""
        (knoten1, knoten2) = kante
        if knoten1 in self.__graph_dict:
            self.__graph_dict[knoten1].append(knoten2)
        else:
            self.__graph_dict[knoten1] = [knoten2]
        
    def __generiereKanten(self):
        """ eine statische Methode die zum Erstellen der Kanten des Graphs, die in einer Liste zurückgegeben werden """ 
        kanten = []
        for knoten in self.__graph_dict:
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
    
    def zeichne(self, startpunkt:tuple, zielpunkt:tuple, liste_verbindungen: list):
        # Koordinaten werden um diesen Faktor erweitert, damit sie auf der Zeichenfläche sichtbar sind
        FACTOR = 100
        RADIUS = 20
        
        # Anfangspunkt
        anfangspunkt = self.kreis(canvas=self, x=startpunkt[0]*FACTOR, y=startpunkt[1]*FACTOR, radius=RADIUS)
        zielpunkt = self.kreis(canvas=self, x=zielpunkt[0]*FACTOR, y=zielpunkt[1]*FACTOR, radius=RADIUS)
        for punkt in liste_verbindungen:
            self.kreis(canvas=self, x=punkt[0]*FACTOR, y=punkt[1]*FACTOR, radius=RADIUS)
        #TODO: diese punkte in liste_verbindungen sind ja die Punkte
        #TODO: Verbindungen zwischen den einzelnen Punkten machen
        #TODO: Speicherung in einem Graph vllt

    def kreis(self, canvas, x, y, radius):
        id = canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill="red")
        return id
          
     
    
                 
        


if __name__ == "__main__":
    root = Tk()
    EingabeFenster(root).pack(side="top", fill="both", expand=True)
    root.mainloop()    


























#class Berechnungen:


    
    
    
    
    
    
    
    
    
    
    
    
    

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
            