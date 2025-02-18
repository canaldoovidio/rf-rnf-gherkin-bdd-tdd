class RouteOptimizer:
    """
    Simula o cálculo de uma rota alternativa para um caminhão.
    """

    def __init__(self):
        self.alternative_requested = False

    def request_alternative(self, truck_id):
        self.alternative_requested = True
        print(f"Calculando rota alternativa para o caminhão {truck_id}")
        return f"Rota alternativa para {truck_id}"
