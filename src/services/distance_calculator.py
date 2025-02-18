import math
# Importa o módulo math para usar funções matemáticas, como radianos, seno, cosseno e arctangente.

class DistanceCalculator:
    # Define a classe DistanceCalculator, responsável por calcular a distância entre duas coordenadas GPS.
    """
    Responsável por calcular distâncias entre coordenadas GPS.
    Aspectos ISO 25010:
    - Confiabilidade: utiliza fórmula reconhecida (Haversine).
    - Eficiência: cálculo rápido em tempo constante.
    """

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # Método que calcula a distância entre duas coordenadas (lat1, lon1) e (lat2, lon2) usando a fórmula de Haversine.
        
        R = 6371  # Define o raio médio da Terra em quilômetros.
        
        d_lat = math.radians(lat2 - lat1)
        # Calcula a diferença entre as latitudes (em graus) e converte essa diferença para radianos.
        
        d_lon = math.radians(lon2 - lon1)
        # Calcula a diferença entre as longitudes (em graus) e converte essa diferença para radianos.
        
        a = (math.sin(d_lat / 2) ** 2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            (math.sin(d_lon / 2) ** 2)
        # Calcula o valor intermediário 'a' da fórmula de Haversine:
        # - Calcula o quadrado do seno da metade da diferença de latitude.
        # - Multiplica o cosseno das latitudes (convertidas para radianos) e o quadrado do seno da metade da diferença de longitude.
        # - Soma os dois termos.
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        # Calcula o ângulo central 'c' usando a função arctan2,
        # que retorna o ângulo cujo seno e cosseno são dados pelos valores calculados.
        
        distance = R * c
        # Calcula a distância final multiplicando o raio da Terra pelo ângulo central 'c' obtido.
        
        return distance
        # Retorna a distância calculada entre os dois pontos, em quilômetros.
