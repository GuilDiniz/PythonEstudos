from rich import print, inspect
class Avaliacao:
    def __init__(self, nome, disciplina, nota = 0):
        self.nome = nome 
        self.disciplina = disciplina
        self._nota = nota

    # Criando Atributo Validável
    @property
    def nota(self): 
        return self._nota
    
    @nota.setter
    def nota(self, nota): 
        if 0 <= nota <= 10:
            self._nota = nota
        else:
            print("NOTA NÃO PERMITIDA!")



'''
    # Métodos Acessores
    def get_nota(self): # Método Getter
        return self._nota
    
    def set_nota(self, nota): # Método Setter
        if 0 <= nota <= 10:
            self._nota = nota   
        else:
            print("nota não permitida")
'''