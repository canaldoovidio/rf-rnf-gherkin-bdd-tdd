from behave import given, when, then
from src.services.deviation_analyzer import DeviationAnalyzer
from src.services.route_optimizer import RouteOptimizer

@given('que tenho um conjunto de rotas planejadas no sistema')
def step_setup_planned_routes(context):
    # Setup inicial: carregamos as rotas planejadas (mock ou real)
    context.planned_routes = {
        "CX123": {
            "coordinates": [
                # Exemplo de coordenadas planejadas (latitude, longitude)
                (10.000, 20.000),
                (10.005, 20.010),
                (10.010, 20.020)
            ]
        }
    }

@given('cada rota possui coordenadas pré-definidas')
def step_assert_routes_predefined(context):
    assert "CX123" in context.planned_routes

@given('o caminhão "{truck_id}" está em rota planejada')
def step_truck_in_route(context, truck_id):
    context.truck_id = truck_id
    context.deviation_analyzer = DeviationAnalyzer()
    context.route_optimizer = RouteOptimizer()

@when('recebo 3 atualizações de localização com desvio de 7 km da rota')
def step_receive_3_deviations(context):
    # Simular 3 leituras de localização com 7 km de desvio
    # Em um caso real, usaríamos mocks ou stubs
    context.deviations = [7.0, 7.0, 7.0]  # 3 leituras
    for dist in context.deviations:
        context.deviation_analyzer.process_location_update(
            truck_id=context.truck_id,
            distance_from_route=dist
        )

@then('devo registrar o desvio no DeviationRepository')
def step_assert_deviation_registered(context):
    # Verificar se o desvio foi registrado (ex.: chamando um método ou checando logs)
    assert context.deviation_analyzer.deviation_detected is True, "Desvio não foi detectado!"

@then('devo enviar uma notificação de alerta')
def step_assert_alert_notification(context):
    # Verificar se o sistema enviou notificação
    # Aqui pode-se verificar flags ou mocks de NotificationManager
    assert context.deviation_analyzer.notification_sent is True, "Notificação não foi enviada!"

@then('devo solicitar uma rota alternativa ao RouteOptimizer')
def step_assert_alternative_route_requested(context):
    # Verificar se a rota alternativa foi solicitada
    # Pode ser um mock no route_optimizer
    assert context.route_optimizer.alternative_requested is True, "Não foi solicitada rota alternativa!"
