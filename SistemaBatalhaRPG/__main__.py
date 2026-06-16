from personagem_rpg import *

def main():
        p1 = Guerreiro("Goku", 1000)
        p2 = Mago("Patolino", 1000)
        while True:
            n = random.randint(1,4)
            if n == 1:
                p2.atacar(p1, 500)
            elif n == 2:
                p1.atacar(p2,500)
            elif n == 3:
                p2.curar()
            elif n == 4:
                p1.curar()
            if p1.morte() or p2.morte():
                 break
if __name__ == "__main__":
    main()