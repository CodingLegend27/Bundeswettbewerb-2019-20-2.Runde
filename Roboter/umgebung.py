eingabe = """
5
3,5,9
3
5,1,3
1,2,2
5,4,3
"""
# erste Zeile: Größe des Spielbretts (quadratisch)
# zweite Zeile: Koordinaten des Robotors und die Ladung seiner Batterie
# dritte Zeile: Anzahl der restlichen Batterien, die auf dem Spielfeld verteilt sind
# ab der vierten Zeile: Koordinaten einer Batterie, zusammen mit ihrer Ladung
# Schreibweise: x-Koordinate, y-Koordinate, Ladung


class Environment:
    def __init__(self, eingabe: str):
        """ erstellt eine Umgebung mit der gegebenen Eingabe im Format, siehe oben (oder auf der BwInf-Website) """
        eingabe = eingabe.rsplit()
        self.size = eingabe.pop(0)
        
        # Die Positon des Roboters oder der Batterien werden in einem Tuple der Form (x, y, ladung) gespeichert
        self.roboter = (eingabe.pop(0) for i in range(3))
        self.anzahl_batterien = eingabe.pop(0)
        # die restlichen Batterien werden hinzugefügt
        self.batterien = []
        for n in range(self.anzahl_batterien):
            self.batterien.append(
                (eingabe.pop(0) for i in range(3))
            )
        
    def move()
        
