e = ['(0,0)', '(1,1)']

e.pop(0)
def zuPunkt(eingabe):
    """ verwertet die Eingabe zu einem Punkt der als Tuple aufgebaut ist
        z.B.: '('0','0') wird zum Tuple (0,0) umgewandelt """    
    print(eingabe)
    return (
        int(list(eingabe)[1]),
        int(list(eingabe)[3])
        )

f = [zuPunkt(e[0])]

print(f)


for i in 10:
    print(i)