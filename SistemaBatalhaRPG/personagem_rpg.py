from abc import ABC, abstractmethod
from rich import print
import random


class Personagem(ABC):

    def __init__(self, nome, vida):
        self.nome = nome
        self.vida = vida
        self.golpes = []
        self.vivo = True
    
    def resumo(self):
        print(f"{self.nome} está com {self.vida} pontos de vida")
    
    def morte(self):
        if self.vida == 0:
            print(f"[red]{self.nome} está morto[/]")
            self.vivo = False
            return True

    def atacar(self, alvo, forca):
        if self.vivo and alvo.vivo:
            #vai ter um um ataque
            golpe = self.golpes[random.randrange(0, len(self.golpes))]
            print (f"[blue]{self.nome}[/] atacou [green]{alvo.nome}[/] com um{golpe}")
            alvo.receber_dano(forca)
            print("="*30)
            self.resumo()
            alvo.resumo()
            print("="*30)

    def receber_dano(self, dano):
        if self.vivo:
            valor = random.randint(0,dano)
            self.vida = self.vida - valor
            print(f"{self.nome} recebeu um dano de [red]{valor}[/]")
            if self.vida < 0:
                self.vida = 0
            return self.vida, self.vivo
    
    @abstractmethod
    def curar(self):
        pass


class Guerreiro(Personagem):

    def __init__(self, nome, vida):
        super().__init__(nome, vida)
        self.golpes = [" [red]Soco[/]", " [red]Chute[/]", "a [red]Voadora[/]"]
    
    def curar(self):
        if self.vida != 0:
            valor = random.randint(0,50)
            self.vida += valor
            print(f"{self.nome} usou um kit médico e recuperou {valor} pontos de vida")
            return self.vida

class Mago(Personagem):

    def __init__(self, nome, vida):
        super().__init__(nome, vida)
        self.golpes = [f"a [red]Bola de Fogo[/]", " [red]Raio de Gelo[/]", "a [red]Explosão[/]"]

    def curar(self):
        if self.vida != 0:
            valor = random.randint(0,50)
            self.vida += valor
            print(f"{self.nome} usou magia de cura e recuperou {valor} pontos de vida")