from rich import print

class ContaBancaria:
    """
    Cria uma conra bancária permitindo fazer sauqes e depósitos
    """
    def __init__(self, id, nome, saldo = 0):
        self.id = id
        self.titular = nome
        self.saldo = saldo
        print(f"Conta {self.id} criada com sucesso. Saldo atual de R${self.saldo:,.2f}")
    
    def __str__(self):  
        return f"A conta {self.id} de {self.titual} tem R${self.saldo:,.2f} de saldo."
    
    def depositar(self, valor):
        self.saldo += valor
        print(f"Depósito de R${valor:,.2f} autorizado na conta {self.id}. \n Saldo atual de R${self.saldo:,.2f}")

    def sacar(self, valor):
        if valor > self.saldo:
            print(f"[red]SAQUE CONTESTADO, SALDO INSUFICIENTE[/]")
        else:
            self.saldo -= valor
            print(f"Saque de R${valor:,.2f} autorizado na conta {self.id}. \n Saldo atual de R${self.saldo:,.2f}")