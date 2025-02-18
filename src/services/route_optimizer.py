class RouteOptimizer:
    # Define a classe RouteOptimizer, que simula o cálculo de uma rota alternativa para um caminhão.
    """
    Simula o cálculo de uma rota alternativa para um caminhão.
    """

    def __init__(self):
        # Método construtor da classe, chamado ao criar uma nova instância.
        self.alternative_requested = False
        # Inicializa o atributo alternative_requested como False, indicando que nenhuma rota alternativa foi solicitada ainda.

    def request_alternative(self, truck_id):
        # Método que simula o cálculo e a solicitação de uma rota alternativa para o caminhão.
        # truck_id: identificador do caminhão para o qual será calculada a rota alternativa.
        self.alternative_requested = True
        # Atualiza o atributo alternative_requested para True, sinalizando que a rota alternativa foi solicitada.
        print(f"Calculando rota alternativa para o caminhão {truck_id}")
        # Exibe uma mensagem no console informando que está calculando a rota alternativa para o caminhão identificado.
        return f"Rota alternativa para {truck_id}"
        # Retorna uma string simulando a rota alternativa calculada para o caminhão.
