import pytest
from src.services.distance_calculator import DistanceCalculator

@pytest.fixture
def distance_calculator():
    return DistanceCalculator()

def test_calculate_distance_simple(distance_calculator):
    # Dado coordenadas próximas
    lat1, lon1 = 10.000, 20.000
    lat2, lon2 = 10.001, 20.001
    
    distance = distance_calculator.calculate_distance(lat1, lon1, lat2, lon2)
    # Valida se a distância está dentro de um range aceitável (cerca de 0.157 km)
    assert 0.15 < distance < 0.17, "Distância não corresponde ao esperado."

def test_calculate_distance_zero(distance_calculator):
    # Mesmo ponto
    distance = distance_calculator.calculate_distance(10.000, 20.000, 10.000, 20.000)
    assert distance == 0, "Distância deveria ser zero."

def test_calculate_distance_long_range(distance_calculator):
    # Distância entre pontos distantes
    distance = distance_calculator.calculate_distance(10.000, 20.000, 11.000, 21.000)
    # Apenas um teste genérico para garantir que seja maior que zero
    assert distance > 0, "Distância deveria ser maior que zero."
