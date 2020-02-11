# Testprogramm zum Testen des Graphen in abbiegen.py

from abbiegen import Graph, Punkt, Kante

g = Graph()

p1 = Punkt(4, 1)
p2 = Punkt(1, 1)
p3 = Punkt(2, 4)
p4 = Punkt(3, 2)

k1 = Kante(p1, p2)
k5 = Kante(p2, p1)

k2 = Kante(p2, p3)
k6 = Kante(p3, p2)

k3 = Kante(p3, p4)
k7 = Kante(p4, p3)

k4 = Kante(p4, p1)
k8 = Kante(p1, p4)

kanten = [k1, k2, k3, k4, k5, k6, k7, k8]

for k in kanten:
     g.addKante(k)

print("test")

# print("\n Eigenschaften Graph" + str(g) + "\n Knoten" + str(g.Kanten()))
# print("\n Knoten" + str(g.Knoten()))
