from rich import print

class ContaBancaria:
    """
    Cria uma conra bancária permitindo fazer sauqes e depósitos
    """
    def __init__(self, id, nome, saldo = 0):
        self.id = id # Público
        self._titular = nome # Protegido
        self.__saldo = saldo # Privado
        print(f"Conta {self.id} criada com sucesso. Saldo atual de R${self.__saldo:,.2f}")
    
    def __str__(self):  
        return f"A conta {self.id} de {self._titular} tem R${self.__saldo:,.2f} de saldo."
    
    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            print(f"Depósito de R${valor:,.2f} autorizado na conta {self.id}. \n Saldo atual de R${self.__saldo:,.2f}")
        else:
            print("[red]Esse valor não é permitido[/]")

    def sacar(self, valor):
        if valor > 0:
            if valor > self.__saldo:
                print(f"[red]SAQUE CONTESTADO, SALDO INSUFICIENTE[/]")
            else:
                self.__saldo -= valor
                print(f"Saque de R${valor:,.2f} autorizado na conta {self.id}. \n Saldo atual de R${self.   __saldo:,.2f}")
        else:
            print("[red]Esse valor não é permitido[/]")
    