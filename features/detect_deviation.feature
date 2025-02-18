# language: pt

Funcionalidade: Detecção de Desvio de Rota
  Como um sistema de monitoramento de rotas
  Quero analisar as coordenadas recebidas periodicamente
  Para detectar desvios maiores que 6 km em 3 atualizações consecutivas

  Contexto:
    Dado que tenho um conjunto de rotas planejadas no sistema
    E cada rota possui coordenadas pré-definidas

  Cenário: Caminhão desvia mais de 6 km por 3 atualizações consecutivas
    Dado que o caminhão "CX123" está em rota planejada
    Quando recebo 3 atualizações de localização com desvio de 7 km da rota
    Então devo registrar o desvio no DeviationRepository
    E devo enviar uma notificação de alerta
    E devo solicitar uma rota alternativa ao RouteOptimizer
