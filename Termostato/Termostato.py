
class Termostato:
    def __init__(self, temp = 24):
        self.__temperatura = temp # Atributo Privado
        self.ftemperatura = f"{temp}°C" #temperatura formatada

    
    # ------ Getter e setter temperatura----- #
    @property
    def temperatura(self): # Getter 
        return self.__temperatura
    

    @temperatura.setter
    def temperatura(self, temp): # Setter 
        if 16 <= temp <= 30: # Validando de se a temperatura está dentro dos limites
            int_temp = temp // 1 # Criando um método para aproximar a temperatura
            fract_temp = temp - int_temp
            if fract_temp != 0 and fract_temp != 0.5: 
                if 0 < fract_temp <= 0.25:
                    temp = int_temp
                elif 0.25 < fract_temp <= 0.75:
                    temp = int_temp + 0.5
                elif 0.75 < fract_temp < 1:
                    temp = int_temp + 1
            self.__temperatura = temp
            self.ftemperatura = f"{temp}°C"
        elif temp < 16:
            self.__temperatura = 16
            self.ftemperatura = f"16°C"
        elif temp > 30:
            self.__temperatura = 30
            self.ftemperatura = f"30°C"