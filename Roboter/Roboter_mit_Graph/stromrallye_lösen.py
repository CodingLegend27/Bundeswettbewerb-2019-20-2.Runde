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

        self.main2()

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
            erreichbare_batterien = self.erreichbareBatterien(*batterie, restliche_batterien)
            
            # die erreichbaren Batterien bilden zusammen mit der aktuellen Batterie eine Kante,
            # wobei die aktuelle Batterie der Startknoten der Kante und die erreichbare Batterie der Endknoten der Kante ist
            # die Gewichtung der Kante ist die verbrauchte Ladung von der aktuellen Batterie zur erreichbaren Batterie
            for erreichbare_batterie in erreichbare_batterien:
                # nur die x- und y-Koordinaten der Batterien werden benötigt, die Ladung nicht
                x_start, y_start = batterie[:2]
                x_ende, y_ende = erreichbare_batterie[:2]
                
                # verbrauchte Ladung ist die Manhattan-Distanz
                verbrauchte_ladung = self.manhattanDistanz(x_start, y_start, x_ende, y_ende)
                self.graph.add_Kante((x_start, y_start), (x_ende, y_ende), verbrauchte_ladung)
        
        # dasselbe wird ebenfalls für den Roboter durchgeführt
        roboter_erreichbare_batterien = self.erreichbareBatterien(*self.roboter, self.batterien)
        for erreichbare_batterie in roboter_erreichbare_batterien:
            x_start, y_start = self.roboter[:2]
            x_ende, y_ende = erreichbare_batterie[:2]
            verbrauchte_ladung = self.manhattanDistanz(x_start, y_start, x_ende, y_ende)
            self.graph.add_Kante((x_start, y_start), (x_ende, y_ende), verbrauchte_ladung)
        
        aktuelle_ladung_batterien = defaultdict(list)
        for batterie in self.batterien:
            x, y, ladung = batterie
            aktuelle_ladung_batterien[(x, y)] = ladung
        
        aktuelle_ladung_batterien[self.roboter[:2]] = self.roboter[2]
        #längster_pfad = self.bfs(self.graph, (self.roboter[:2]), self.roboter[2], aktuelle_ladung_batterien, self.batterien)
        
        # als Liste der restlichen Batterien werden nur die x- und y-Koordinaten aller Batterien benötigt
        restliche_batterien = list(map(lambda batterie: batterie[:2], self.batterien))
        
        längster_pfad = self.dfs(self.graph, self.roboter[:2], self.roboter[2], aktuelle_ladung_batterien, restliche_batterien)
               
        pass
    
    def dfs(self, graph, start, aktuelle_ladung, aktuelle_ladung_batterien, restliche_batterien, pfad=[]):


        
        pfad.append(start)
        
        if len(pfad)>1:
        # aktualisiere Nachbarknoten des vorherigen Knoten, da sich bei diesem die Ladung geändert hat
            
            restliche_batterien.remove(start)
            
            
            vorheriger_knoten = pfad[-1]
            erreichbare_batterien_neu = self.erreichbareBatterien(*vorheriger_knoten, aktuelle_ladung, restliche_batterien)
            erreichbare_batterien_neu = list(map(
                lambda batterie: (*batterie, self.manhattanDistanz(
                    *batterie, *vorheriger_knoten
                )), erreichbare_batterien_neu
            ))
            graph.aktualisiereNachfolger(vorheriger_knoten, erreichbare_batterien_neu)
            aktuelle_ladung_batterien[vorheriger_knoten] = aktuelle_ladung
            
            if aktuelle_ladung > 0:
                restliche_batterien.append((*vorheriger_knoten, aktuelle_ladung))
        
        
        
        
        
        aktuelle_ladung = aktuelle_ladung_batterien[start]
        
        
        
        
        
        if graph[start]:
            
            # für benachbarte Knoten wird die DFS aufgerufen
            for nachfolger_item in graph[start]:
                knoten, gewichtung = nachfolger_item[0]
                
                # falls der Knoten noch nicht besucht wurde
                if knoten in restliche_batterien:
                   
                    
                    # Ladungsverbrauch wird abgezogen
                    #aktuelle_ladung -= gewichtung
                    
                    
                    self.dfs(graph, knoten, aktuelle_ladung-gewichtung, aktuelle_ladung_batterien, restliche_batterien, pfad)

                # falls alle Batterien besucht wurden
                elif not restliche_batterien:
                    return pfad

        else:
            if not restliche_batterien:
                return pfad
            # else: 
            #     return None
        
            
    def bfs(self, graph, aktueller_knoten, aktuelle_ladung_roboter, aktuelle_ladung_batterien, restliche_batterien, aktueller_pfad=[]):
        
        # # jetzt ändert sich eventuell die erreichbaren Batterien der aktuellen Ersatzbatterie, die ja eine neue Ladung bekommen
        #         erreichbare_batterien_neu = self.erreichbareBatterien(*knoten, aktuelle_ladung_roboter, restliche_batterien)
        #         graph.aktualisiereNachfolger(knoten, erreichbare_batterien_neu)
        
        if graph[aktueller_knoten]:
            
            for nachfolge_item in graph[aktueller_knoten]:
                #if knoten not in aktueller_pfad
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
        ursprüngliche_nachfolger_items = self.adjazenzliste[knoten]
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
        #(4, 3, 2)
    ]

    s = Steuerung(roboter, batterien)
