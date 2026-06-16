from personagem_rpg import *

def main():
        p1 = Guerreiro("Goku", 1000)
        p2 = Mago("Patolino", 800)
        while True:
            p2.atacar(p1, 300)
            p1.atacar(p2,200)
if __name__ == "__main__":
    main()