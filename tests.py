def u(n) :
    return n*1000 + 3000

somme = 0
for i in range(1,36):
    print(i)
    somme += u(i)

somme2 = 0
for i in range(36,51):
    print(i)
    somme2 += u(i)

print(somme,somme2)