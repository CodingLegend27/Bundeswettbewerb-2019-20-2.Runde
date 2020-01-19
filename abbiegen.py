# 2. Runde Bundeswettbewerb Informatik 2019/20
# from PySide2.QtCore import Qt
# from PySide2.QtWidgets import *
from tkinter import *

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
        
        # Daten
        self.anzahl_straßen = None
        self.startpunkt = None
        self.zielpunkt = None
        self.liste_verbindungen = None

    def starte(self):
        eingabe = self.textfeld.get('1.0', 'end').rsplit()
        print(eingabe)
        
        # Zuweisung der Klassenvariablen durch die eingegebenen Daten
        self.anzahl_straßen = int(eingabe.pop(0))
        self.startpunkt = self.zuPunkt(eingabe.pop(0))
        self.zielpunkt = self.zuPunkt(eingabe.pop(0))
        self.liste_verbindungen = []
        for koordinaten in eingabe:
            self.liste_verbindungen.append(
                self.zuPunkt(koordinaten)
            )
        
        print("\nAnzahl der Straßen: ", self.anzahl_straßen)
        print("Startpunkt: ", self.startpunkt)
        print("Zielpunkt: ", self.zielpunkt)
        print("Liste Verbindungen ", self.liste_verbindungen)      
        
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
        
        

    
    def zuPunkt(self, eingabe):
        """ verwertet die Eingabe zu einem Punkt der als Tuple aufgebaut ist
        z.B.: '('0','0') wird zum Tuple (0,0) umgewandelt """    
        return (
            int(list(eingabe)[1]),
            int(list(eingabe)[3])
            )
        
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
            