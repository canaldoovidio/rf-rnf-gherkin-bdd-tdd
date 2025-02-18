import pytest
from unittest.mock import MagicMock
from src.services.deviation_analyzer import DeviationAnalyzer

@pytest.fixture
def deviation_analyzer():
    return DeviationAnalyzer()

def test_no_deviation_detected(deviation_analyzer):
    # Com distâncias abaixo de 6 km, não deve disparar alerta
    distances = [3.0, 4.5, 5.9]
    for d in distances:
        deviation_analyzer.process_location_update("CX123", d)
    assert deviation_analyzer.deviation_detected is False

def test_deviation_detected_after_three_updates(deviation_analyzer):
    # Mock de notificação e rota
    deviation_analyzer._send_notification = MagicMock()
    deviation_analyzer._request_alternative_route = MagicMock()

    distances = [7.0, 7.1, 7.0]
    for d in distances:
        deviation_analyzer.process_location_update("CX123", d)
    assert deviation_analyzer.deviation_detected is True
    deviation_analyzer._send_notification.assert_called_once()
    deviation_analyzer._request_alternative_route.assert_called_once()
