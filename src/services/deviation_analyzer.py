class DeviationAnalyzer:
    """
    Responsável por analisar se há desvio de rota maior que 6 km por 3 atualizações consecutivas.
    ISO 25010:
    - Confiabilidade: lógica clara e testada para detecção de desvio.
    - Manutenibilidade: métodos privados para isolar comportamentos.
    """

    def __init__(self, route_optimizer=None):
        self.consecutive_deviations = 0
        self.deviation_detected = False
        self.notification_sent = False
        self.route_optimizer = route_optimizer

    def process_location_update(self, truck_id, distance_from_route):
        if distance_from_route > 6.0:
            self.consecutive_deviations += 1
        else:
            self.consecutive_deviations = 0

        if self.consecutive_deviations >= 3 and not self.deviation_detected:
            self.deviation_detected = True
            self._send_notification(truck_id)
            self._request_alternative_route(truck_id)

    def _send_notification(self, truck_id):
        self.notification_sent = True
        print(f"Enviando notificação de desvio para o caminhão {truck_id}...")

    def _request_alternative_route(self, truck_id):
        if self.route_optimizer:
            self.route_optimizer.request_alternative(truck_id)
        else:
            print(f"Solicitando rota alternativa para o caminhão {truck_id}...")
