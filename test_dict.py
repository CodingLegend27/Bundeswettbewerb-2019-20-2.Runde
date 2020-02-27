knoten = [
    (0, 2), (0, 1), (1, 1), (0, 3), (1, 1), (1, 3), (1,
                                                     3), (2, 2), (2, 2), (2, 3), (2, 3), (3, 3), (3, 3), (4, 3)
]


zips = zip(knoten, [[1, 0, 3] for i in range(len(knoten))])

besucht = dict(zips)

print(besucht)

sorted(besucht.keys())

print(besucht)

besucht = {k: sorted(besucht[k]) for k in sorted(besucht)}

print(besucht)
