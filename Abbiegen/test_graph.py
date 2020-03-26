from abbiegen_neuerVersuch import *

# g = Graph()
# g.add_Kante(0, 1, 2)
# g.add_Kante(1, 3, 2)
# g.add_Kante(0, 2, 2)


# kanten = g.kanten

# print(kanten)

def chebyshev_distance(start, ende):
    D = 1
    D2 = 1
    dx = abs(start[0] - ende[0])    
    dy = abs(start[1] - ende[1])
    return D*(dx + dy) + (D2 - 2 * D) * min(dx, dy)

p1 = (0, 1)
p2 = (2, 2)
d = chebyshev_distance(p1, p2)

print(d)
    