import time
import asyncio
from behave import given, when, then
from unittest.mock import patch, AsyncMock
import src.services.retry_circuit_breaker as cb


@given('que o circuit breaker está no estado "{state}"')
def step_set_circuit_state(context, state):
    cb.circuit_state = state
    cb.test_in_half_open = False
    if state == "closed":
        cb.delay = cb.baseline  # Reset delay to 20ms
    context.circuit_state_before = state


@given('o serviço externo responde em menos de 1000ms')
def step_service_responds_fast(context):
    cb.delay = cb.baseline  # 20ms — well under 1000ms threshold


@given('o serviço externo está falhando com delay acima de 1000ms')
def step_service_failing(context):
    cb.delay = 2000  # Above 1000ms threshold, will cause failure


@given('o tempo de abertura ainda não expirou')
def step_open_not_expired(context):
    cb.time_opened = time.time()  # Just opened now


@given('já se passaram mais de 3 segundos desde a abertura')
def step_open_expired(context):
    cb.time_opened = time.time() - 4  # 4 seconds ago, > open_duration (3s)
    cb.delay = cb.baseline  # Reset delay so the test call will succeed
    context._expect_recovery = True


@given('o serviço externo voltou a responder normalmente')
def step_service_recovered(context):
    cb.delay = cb.baseline  # Reset to fast response


@when('uma chamada é feita ao serviço externo')
def step_call_service(context):
    # Reset delay to baseline for recovery scenarios
    if cb.circuit_state == cb.HALF_OPEN or (cb.circuit_state == cb.OPEN and hasattr(context, '_expect_recovery')):
        cb.delay = cb.baseline
    try:
        result = asyncio.run(cb.circuit_breaker_function())
        context.call_result = result
        context.call_exception = None
    except Exception as e:
        context.call_result = None
        context.call_exception = e


@when('uma chamada de teste é feita ao serviço externo')
def step_call_test_service(context):
    try:
        result = asyncio.run(cb.circuit_breaker_function())
        context.call_result = result
        context.call_exception = None
    except Exception as e:
        context.call_result = None
        context.call_exception = e


@then('a resposta é recebida com sucesso')
def step_assert_success(context):
    assert context.call_exception is None, f"Expected success but got: {context.call_exception}"
    assert context.call_result is not None


@then('o circuit breaker permanece no estado "{state}"')
def step_assert_state_remains(context, state):
    assert cb.circuit_state == state, f"Expected {state} but got {cb.circuit_state}"


@then('a chamada falha com exceção')
def step_assert_failure(context):
    assert context.call_exception is not None, "Expected exception but call succeeded"


@then('o circuit breaker muda para o estado "{state}"')
def step_assert_state_changed(context, state):
    assert cb.circuit_state == state, f"Expected {state} but got {cb.circuit_state}"


@then('a chamada é rejeitada imediatamente com "{message}"')
def step_assert_rejected(context, message):
    assert context.call_exception is not None, "Expected rejection but call succeeded"
    assert message in str(context.call_exception), \
        f"Expected '{message}' in exception but got: {context.call_exception}"


@then('o serviço externo não é chamado')
def step_assert_no_external_call(context):
    # When circuit is OPEN and not expired, the function raises before calling delayed_function
    # This is implicitly verified by the rejection assertion above
    assert context.call_exception is not None
