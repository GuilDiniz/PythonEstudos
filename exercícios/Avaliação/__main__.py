from Avaliacao import *

def main():
    av1 = Avaliacao("Pedro", "Matemática")
    av1.nota = 7.4
    print(f"{av1.nome} tirou {av1.nota} na prova de {av1.disciplina}")
    inspect(av1, private= True)

if __name__ == "__main__":
    main()