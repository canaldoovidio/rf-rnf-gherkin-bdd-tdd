class DeviationAnalyzer:
    """
    Responsável por analisar se há desvio de rota maior que 6 km por 3 atualizações consecutivas.
    ISO 25010:
    - Confiabilidade: lógica clara e testada para detecção de desvio.
    - Manutenibilidade: métodos privados (_send_notification, _request_alternative_route) para isolar comportamentos.
    """

    def __init__(self):
        self.consecutive_deviations = 0
        self.deviation_detected = False
        self.notification_sent = False

    def process_location_update(self, truck_id, distance_from_route):
        """
        Processa cada atualização de localização, verificando se a distância excede 6 km.
        """
        if distance_from_route > 6.0:
            self.consecutive_deviations += 1
        else:
            self.consecutive_deviations = 0

        if self.consecutive_deviations >= 3 and not self.deviation_detected:
            self.deviation_detected = True
            self._send_notification(truck_id)
            self._request_alternative_route(truck_id)

    def _send_notification(self, truck_id):
        """
        Simula envio de notificação ao NotificationManager.
        """
        # Lógica de integração com NotificationManager
        self.notification_sent = True
        print(f"Enviando notificação de desvio para o caminhão {truck_id}...")

    def _request_alternative_route(self, truck_id):
        """
        Simula solicitação de rota alternativa ao RouteOptimizer.
        """
        print(f"Solicitando rota alternativa para o caminhão {truck_id}...")

