import math



def berechneSteigungKante(kante: tuple):
    """berechnet die Steigung der eingegebenen Kante."""
    # Differenz der y-Koordinaten des Start- und Zielpunktes der gegebenen Kante
    y_diff = kante[0][1] - kante[1][1]

    # Differenz der x-Koordinaten des Start- und Zielpunktes der gegebenen Kante
    x_diff = kante[0][0] - kante[1][0]
    try:
        steigung = y_diff / x_diff
    # falls keine Veränderung in x-Richtung vorliegt, wird der Steigung die 'Zahl' unendlich zugewiesen
    except ZeroDivisionError:
        steigung = math.inf

    return steigung


def berechneAnzahlAbbiegenPfad(pfad: list):
    """ Berechnung der Anzahl, wie häufig auf dem gegebenen Pfad (Liste von Punkten = Parameter) abgebogen werden muss
    """
    # Liste mit allen Steigungen der gegebenen Strecken wird erstellt
    steigungen = []
    # dabei wird die Methode berechneSteigungKante(tuple) aufgerufen
    for i in range(len(pfad)):
        if i > 0:
            steigungen.append(
                berechneSteigungKante((pfad[i-1], pfad[i]))
            )

    # die Anzahl der Abbiegevorgänge beträgt zu Beginn 0
    anzahl_abbiegen = 0
    # TODO kommentare
    for i in range(len(steigungen)):
        # die Steigung der akutellen Strecke wird zugewiesen
        aktuell = steigungen[i]
        # falls es Strecke vor der aktuellen Strecke gibt
        if i > 0:
            # die Steigung der Strecke vor der aktuellen Strecke wird zugewiesen
            zuvor = steigungen[i-1]
            # wenn die beiden zugewiesenen Steigungen unterschiedlich sind,
            # wird der Zähler erhöht
            if aktuell != zuvor:
                anzahl_abbiegen += 1

    # while steigungen:
    #     aktuell = steigungen[-1]
    #     zuvor = next(aktuell, None)
    #     if aktuell != zuvor:
    #         anzahl_abbiegen +=1
    # Rückgabewert: die Anzahl der Abbiegevorgänge im gegebenen Pfad
    return anzahl_abbiegen


def berechneLänge(p1: tuple, p2: tuple):
    # c² = a² + b² wird angewendet (Pythagoras)
    return math.sqrt(
        (p1[0] - p2[0])**2
        +
        (p1[1] - p2[1])**2
    )


def berechneLängePfad(pfad: list):
    """ berechnet die Summe der Teilverbindungen des gegebenen Pfad
    """
    sum = 0
    for i in range(len(pfad)):
        if i > 0:
            sum += berechneLänge(pfad[i-1], pfad[i])
    return sum


alle_pfade = [
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 2), (2, 3), (3, 3), (4, 3)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 2), (3, 3), (4, 3)],
    [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 2), (2, 3), (3, 3), (4, 3)],
    [(0, 0), (0, 1), (0, 2), (1, 1), (2, 2), (3, 3), (4, 3)],
    [(0, 0), (0, 1), (0, 2), (1, 3), (2, 2), (2, 3), (3, 3), (4, 3)],
    [(0, 0), (0, 1), (0, 2), (1, 3), (2, 2), (3, 3), (4, 3)],
    [(0, 0), (0, 1), (0, 2), (1, 3), (2, 3), (3, 3), (4, 3)],
    [(0, 0), (0, 1), (1, 1), (2, 2), (2, 3), (3, 3), (4, 3)],
    [(0, 0), (0, 1), (1, 1), (2, 2), (3, 3), (4, 3)]
]

# die Pfade in alle_pfade werden zu Tuples konvertiert und sind somit hashable und als key für ein Dictionary möglich
alle_pfade = [tuple(pfad) for pfad in alle_pfade]
    

# zu dieser Liste werden die Länge und die Anzahl der Abbiegevorgänge jedes einzelnen Pfades gespeichert
länge_anzahlAbbiegen_alle_pfade = []

for verbindung in alle_pfade:
    länge_anzahlAbbiegen_alle_pfade.append(
        [
            berechneLängePfad(verbindung),
            berechneAnzahlAbbiegenPfad(verbindung)
        ]
    )

zipObj = zip(alle_pfade, länge_anzahlAbbiegen_alle_pfade)

eigenschaften_alle_pfade = dict(zipObj)

print(eigenschaften_alle_pfade)

print("\n", eigenschaften_alle_pfade.items())
# eigenschaften_alle_pfade.items() liefert beispielsweise:
# (
#   (
#       (0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 2), (2, 3), (3, 3), (4, 3)
#   ), 
#       [8.414213562373096, 4]
# )
# das Tuple ist wie folgt aufgebaut: (pfad, [länge_pfad, anzahl_abbiegen])

# die kürzeste Strecke wird gefunden, indem die kleinste Zahl des ersten Elements der Eigenschaften-Liste des Tuples ermittelt wird
pfad_kürzesteStrecke = min(eigenschaften_alle_pfade.items(), key=lambda x: x[1][0])
print("Pfad mit kürzester Strecke: ", pfad_kürzesteStrecke)
länge_kürzeste_Strecke = pfad_kürzesteStrecke[1][0]
print("Länge dieses Pfads: ", länge_kürzeste_Strecke)

# von der kürzesten Strecke ausgehend, werden diejenigen Strecken ausgewählt, die noch im Bereich der eingegebenen maximalen Verlängerung sind
max_verlängerung = float(input("Maximale Verlängerung in Prozent: ")) /100

# die Länge eines Weges mit maximaler Verlängerung wird mithilfe der eingegebenen maximalen Verlängerung berechnet
maximale_länge = länge_kürzeste_Strecke*max_verlängerung + länge_kürzeste_Strecke
print(maximale_länge)

# von dem Dictionary werden nun alle Pfade entfernt, deren Länge größer als die maximal zulässige Länge
# Umsetzung: von dem Dictionary wird eine Kopie erstellt, durch dessen Items mithilfe einer for-Schleife iteriert wird
for pfad in eigenschaften_alle_pfade.copy().items():
    # ist die Länge des Pfades länger als die maximale Länge, wird der Pfad entfernt
    if pfad[1][0] > maximale_länge:
        eigenschaften_alle_pfade.pop(pfad[0])

print("Aktualisierte Pfade: ", eigenschaften_alle_pfade)

# von dem aktualisiertem Dictionary wird nun derjenige Pfad ausgewählt, bei welchem man am wenigsten abbiegen muss
# die kleinste Zahl des zweiten Elements der Eigenschaften-Liste des Tuples liefert hierfür Auskunft über die Anzahl der Abbiegevorgänge im jeweiligen Pfad
# dieser Pfad ist somit der optimalste Weg für Bilal
optimaler_pfad = min(eigenschaften_alle_pfade.items(), key=lambda x: x[1][1])
print(optimaler_pfad)

# Berechnung, um wie viel Prozent der optimalste Weg länger ist als der kürzeste Weg (in Prozent):
umweg = (optimaler_pfad[1][0]-länge_kürzeste_Strecke)/länge_kürzeste_Strecke
print(f"zufahrender Umweg auf optimalstem Weg (im Vergleich zur kürzesten Strecke): {umweg*100} Prozent")

