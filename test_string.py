e = '(14,0)'
i = e.find(',')
print(e[i])
x = e[1:e.find(',')]
y = e[e.find(',')+1:-1]
print(x, y)

print(e)