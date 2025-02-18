class DeviationAnalyzer:
    # Define a classe DeviationAnalyzer, responsável por analisar desvios de rota.
    """
    Responsável por analisar se há desvio de rota maior que 6 km por 3 atualizações consecutivas.
    ISO 25010:
    - Confiabilidade: lógica clara e testada para detecção de desvio.
    - Manutenibilidade: métodos privados para isolar comportamentos.
    """

    def __init__(self, route_optimizer=None):
        # Método construtor da classe.
        # Inicializa os atributos da instância. Pode receber uma instância de route_optimizer, caso haja injeção de dependência.
        self.consecutive_deviations = 0  # Inicializa o contador de atualizações consecutivas com desvio acima de 6 km.
        self.deviation_detected = False  # Flag para indicar se o desvio já foi detectado.
        self.notification_sent = False   # Flag para indicar se a notificação de desvio já foi enviada.
        self.route_optimizer = route_optimizer  # Armazena a instância do otimizador de rota para solicitar rotas alternativas.

    def process_location_update(self, truck_id, distance_from_route):
        # Método responsável por processar cada atualização de localização recebida.
        # truck_id: identificador do caminhão.
        # distance_from_route: distância atual do caminhão em relação à rota planejada.
        if distance_from_route > 6.0:
            # Se a distância for maior que 6 km, incrementa o contador de desvios consecutivos.
            self.consecutive_deviations += 1
        else:
            # Caso contrário, reinicia o contador, pois a atualização não configura um desvio.
            self.consecutive_deviations = 0

        # Se o contador atingir 3 atualizações consecutivas com desvio e o desvio ainda não tiver sido detectado...
        if self.consecutive_deviations >= 3 and not self.deviation_detected:
            self.deviation_detected = True  # Marca que o desvio foi detectado.
            self._send_notification(truck_id)  # Chama o método privado para enviar uma notificação de alerta.
            self._request_alternative_route(truck_id)  # Chama o método privado para solicitar uma rota alternativa.

    def _send_notification(self, truck_id):
        # Método privado para enviar uma notificação de alerta de desvio.
        # Em um cenário real, este método integraria com um sistema de notificações.
        self.notification_sent = True  # Atualiza a flag para indicar que a notificação foi enviada.
        print(f"Enviando notificação de desvio para o caminhão {truck_id}...")
        # Imprime uma mensagem simulando o envio da notificação.

    def _request_alternative_route(self, truck_id):
        # Método privado para solicitar uma rota alternativa.
        # Se uma instância de route_optimizer foi fornecida...
        if self.route_optimizer:
            self.route_optimizer.request_alternative(truck_id)
            # Chama o método request_alternative do otimizador de rota para calcular e solicitar a rota alternativa.
        else:
            # Se não houver um otimizador injetado, apenas imprime uma mensagem simulando a solicitação.
            print(f"Solicitando rota alternativa para o caminhão {truck_id}...")
