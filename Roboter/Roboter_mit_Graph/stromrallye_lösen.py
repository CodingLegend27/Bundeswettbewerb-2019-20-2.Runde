# 2. Runde Bundeswettbewerb Informatik 2019/20
from collections import defaultdict


#https://de.wikipedia.org/wiki/L%C3%A4ngster_Pfad
# 

# <BAUM>
# machen :D
' #TODO# '


class Steuerung:
    def __init__(self, roboter: list, batterien: list):
        # Aufbau: (x, y, ladung)
        self.roboter = roboter
        # Aufbau: [(x1, y1, ladung1), (x2, y2, ladung2), ...]
        self.batterien = batterien

        self.main()

    def erreichbareBatterien(self, x: int, y: int, ladung: int, restliche_batterien: list):
        """ mithilfe der Manhattan-Distanz werden alle Batterien ermittelt,
            von dem gegebenen Standort aus erreichbar sind
            --> der Betrag der Manhattan-Distanz gibt hier in dieser Aufgabe Auskunft darüber,
                wie viel Ladung zwischen zwei Positionen (zur Ersatzbatterie) benötigt wird
        """
        # die gegebene Ladung ist der maximal mögliche Betrag der Manhattan-Distanz
        # daher werden alle Batterien herausgefiltert, dessen Manhattan-Distanz größer als die gegebene Ladung ist
        # und die Distanz größer als 0 ist, damit sie sich nicht selbst als erreichbare Batterie sieht
        erreichbare_batterien = list(filter(
            lambda batterie_item: self.manhattanDistanz(
                x, y, batterie_item[0], batterie_item[1]) <= ladung and self.manhattanDistanz(
                x, y, batterie_item[0], batterie_item[1]) > 0, restliche_batterien
        ))
        return erreichbare_batterien

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
            lambda batterie: self.anzahlErreichbarerBatterien(*batterie, restliche_batterien), erreichbare_batterien
        ))
        
        # # https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-13.php
        
        # dieses Dictionary enthält die jeweiligen erreichbaren Dictionary als Key (x, y, ladung) 
        # und mit der Anzahl der von ihnen aus erreichbaren nächsten Batterien als Key
        # z.B. (5, 1, 3): 1 --> bedeutet, dass von der Batterie mit Koordinaten (5, 1) und Ladung=3 aus eine Batterie erreichbar ist
        erreichbare_batterien_mit_anzahl_nachfolger =  dict(zip(erreichbare_batterien, anzahl_nachfolgende_batterien))
        
        # die erreichbare Batterie mit der höchsten Anzahl an nächsten Batterien wird ausgewählt
        nächste_batterie = max(erreichbare_batterien_mit_anzahl_nachfolger)
        
        # Roboter "geht" zur nächsten Batterie
        # verbrauchte Ladung auf dem Weg zur Batterie wird berechnet
        verbrauchte_ladung = self.manhattanDistanz(*self.roboter[0:2], *nächste_batterie[0:2])
        
        # die verbrauchte Ladung wird von der Bordbatterie des Roboters abgezogen
        self.roboter[2] -= verbrauchte_ladung
        
        # die Ersatzbatterie am Boden wird mit der aktuellen Ladung der Bordbatterie getauscht
        ehemalige_bordbatterie_ladung = self.roboter[2]
        
        # die Ersatzbatterie wird aus den restlichen Batterien entfernt und ist jetzt die Bordbatterie des Roboters
        restliche_batterien.remove(nächste_batterie)
        self.roboter = nächste_batterie
        
        # zu den restlichen Batterien wird die jetzt am Boden liegende Ladung hinzugefügt, die die Ladung der ehemaligen Bordbatterie hat
        restliche_batterien.append(self.roboter[2].insert(2, ehemalige_bordbatterie_ladung))
        
        # Breitensuche gutes Video https://www.youtube.com/watch?v=7RCp2jNwxjQ
        
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



if __name__ == '__main__':
    eingabe = """
    5
    3,5,9
    3
    5,1,3
    1,2,2
    5,4,3
    """
    size = 5
    roboter = (3, 5, 9)
    anzahl_batterien = 3
    batterien = [
        (5, 1, 3),
        (1, 2, 2),
        (5, 4, 3),
        (4, 3, 2)
    ]

    s = Steuerung(roboter, batterien)
