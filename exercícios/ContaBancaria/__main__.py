from ContaBancaria import *


def main():
    c1 = ContaBancaria(111, "Laís", 5000)
    c1.depositar(500)
    c1.sacar(100)

if __name__ == "__main__":
    main()