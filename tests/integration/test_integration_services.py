"""
Testes de integração entre services.
Verificam que os módulos se conectam corretamente (integração interna).
"""
import pytest
from unittest.mock import MagicMock, patch
from src.services.deviation_analyzer import DeviationAnalyzer
from src.services.route_optimizer import RouteOptimizer
from src.services.distance_calculator import DistanceCalculator


class TestIntegrationDeviationAnalyzerRouteOptimizer:
    """Testa a integração entre DeviationAnalyzer e RouteOptimizer."""

    def test_analyzer_calls_optimizer_on_deviation(self):
        """Quando desvio é detectado, o analyzer deve chamar o optimizer."""
        optimizer = RouteOptimizer()
        analyzer = DeviationAnalyzer(route_optimizer=optimizer)

        # Simula 3 atualizações com desvio > 6 km
        for _ in range(3):
            analyzer.process_location_update("CX123", 7.0)

        assert analyzer.deviation_detected is True
        assert optimizer.alternative_requested is True

    def test_analyzer_works_without_optimizer(self):
        """Analyzer funciona mesmo sem optimizer injetado (degradação graciosa)."""
        analyzer = DeviationAnalyzer(route_optimizer=None)

        for _ in range(3):
            analyzer.process_location_update("CX123", 7.0)

        assert analyzer.deviation_detected is True
        assert analyzer.notification_sent is True

    def test_optimizer_receives_correct_truck_id(self):
        """O optimizer recebe o truck_id correto do analyzer."""
        mock_optimizer = MagicMock()
        analyzer = DeviationAnalyzer(route_optimizer=mock_optimizer)

        for _ in range(3):
            analyzer.process_location_update("TRUCK-456", 8.0)

        mock_optimizer.request_alternative.assert_called_once_with("TRUCK-456")

    def test_analyzer_does_not_call_optimizer_without_deviation(self):
        """Sem desvio, o optimizer não deve ser chamado."""
        mock_optimizer = MagicMock()
        analyzer = DeviationAnalyzer(route_optimizer=mock_optimizer)

        # Distâncias abaixo do threshold
        for d in [3.0, 4.5, 5.9]:
            analyzer.process_location_update("CX123", d)

        mock_optimizer.request_alternative.assert_not_called()

    def test_analyzer_detects_only_once(self):
        """O desvio é detectado apenas uma vez, mesmo com updates adicionais."""
        mock_optimizer = MagicMock()
        analyzer = DeviationAnalyzer(route_optimizer=mock_optimizer)

        # 6 atualizações com desvio (2x o mínimo necessário)
        for _ in range(6):
            analyzer.process_location_update("CX123", 7.0)

        # Deve ter chamado o optimizer apenas uma vez
        mock_optimizer.request_alternative.assert_called_once()


class TestIntegrationDeviationAnalyzerDistanceCalculator:
    """Testa a integração conceitual entre DeviationAnalyzer e DistanceCalculator."""

    def test_distance_calculator_provides_realistic_values(self):
        """DistanceCalculator retorna valores que fazem sentido para o DeviationAnalyzer."""
        calc = DistanceCalculator()

        # Dois pontos próximos (~1.5 km) — não deveria disparar desvio
        distance_small = calc.calculate_distance(-23.5505, -46.6333, -23.5600, -46.6400)
        assert distance_small < 6.0, f"Expected < 6 km but got {distance_small}"

        # Dois pontos distantes (~111 km) — deveria disparar desvio
        distance_large = calc.calculate_distance(-23.5505, -46.6333, -22.5505, -46.6333)
        assert distance_large > 6.0, f"Expected > 6 km but got {distance_large}"

    def test_end_to_end_deviation_with_calculated_distances(self):
        """Fluxo completo: DistanceCalculator calcula → DeviationAnalyzer detecta."""
        calc = DistanceCalculator()
        optimizer = RouteOptimizer()
        analyzer = DeviationAnalyzer(route_optimizer=optimizer)

        # Coordenadas planejadas vs reais (desvio grande)
        planned = (-23.5505, -46.6333)
        actual_positions = [
            (-23.6505, -46.7333),  # ~13.6 km de distância
            (-23.6505, -46.7333),
            (-23.6505, -46.7333),
        ]

        for actual in actual_positions:
            distance = calc.calculate_distance(
                planned[0], planned[1], actual[0], actual[1]
            )
            analyzer.process_location_update("CX789", distance)

        assert analyzer.deviation_detected is True
        assert optimizer.alternative_requested is True


class TestIntegrationRouteOptimizer:
    """Testa o RouteOptimizer isoladamente."""

    def test_optimizer_returns_route_string(self):
        """O optimizer retorna uma string com a rota alternativa."""
        optimizer = RouteOptimizer()
        result = optimizer.request_alternative("CX123")

        assert "CX123" in result
        assert optimizer.alternative_requested is True

    def test_optimizer_starts_with_no_request(self):
        """O optimizer inicia sem nenhuma rota alternativa solicitada."""
        optimizer = RouteOptimizer()
        assert optimizer.alternative_requested is False
