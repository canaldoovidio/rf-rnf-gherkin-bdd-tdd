import math

class DistanceCalculator:
    """
    Responsável por calcular distâncias entre coordenadas GPS.
    Aspectos ISO 25010:
    - Confiabilidade: utiliza fórmula reconhecida (Haversine).
    - Eficiência: cálculo rápido em tempo constante.
    """

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # Fórmula de Haversine (exemplo simplificado)
        R = 6371  # Raio médio da Terra em km
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = (math.sin(d_lat / 2) ** 2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            (math.sin(d_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance
