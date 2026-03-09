import time
import asyncio
from behave import given, when, then
import src.services.retry_circuit_breaker as cb


@given('que o serviço externo está funcionando normalmente com delay de 20ms')
def step_service_normal(context):
    cb.delay = 20
    cb.baseline = 20
    cb.time_error_occurred = None
    cb.circuit_state = cb.CLOSED


@given('que o delay inicial é 20ms')
def step_initial_delay(context):
    cb.delay = 20
    cb.baseline = 20
    cb.time_error_occurred = None
    cb.circuit_state = cb.CLOSED


@given('que o delay acumulado excedeu 1000ms')
def step_delay_exceeded(context):
    cb.delay = 2000  # Above 1000ms threshold
    cb.time_error_occurred = None
    cb.circuit_state = cb.CLOSED


@given('que o serviço falhou e registrou o tempo do erro')
def step_service_failed(context):
    cb.delay = 2000
    cb.time_error_occurred = time.time() * 1000  # in milliseconds
    cb.circuit_state = cb.CLOSED


@given('que já se passaram mais de 5 segundos desde o erro')
def step_time_passed(context):
    # Set error time to 6 seconds ago (in ms)
    cb.time_error_occurred = (time.time() - 6) * 1000


@when('uma chamada é feita via delayed_function')
def step_call_delayed(context):
    try:
        result = asyncio.run(cb.delayed_function())
        context.call_result = result
        context.call_exception = None
    except Exception as e:
        context.call_result = None
        context.call_exception = e


@when('uma nova chamada é feita via delayed_function')
def step_call_delayed_new(context):
    try:
        result = asyncio.run(cb.delayed_function())
        context.call_result = result
        context.call_exception = None
    except Exception as e:
        context.call_result = None
        context.call_exception = e


@when('{n:d} chamadas consecutivas são feitas ao serviço')
def step_multiple_calls(context, n):
    context.delays_after = []
    for i in range(n):
        try:
            asyncio.run(cb.delayed_function())
        except Exception:
            pass
        context.delays_after.append(cb.delay)


@then('a resposta contém "{text}"')
def step_assert_response_contains(context, text):
    assert context.call_result is not None, f"Expected response but got exception: {context.call_exception}"
    assert text in context.call_result, f"Expected '{text}' in '{context.call_result}'"


@then('o delay dobra para a próxima chamada')
def step_assert_delay_doubled(context):
    assert cb.delay == 40, f"Expected delay 40 but got {cb.delay}"


@then('o delay após a {nth} chamada é {expected:d}ms')
def step_assert_delay_at_step(context, nth, expected):
    index_map = {"1ª": 0, "2ª": 1, "3ª": 2, "4ª": 3, "5ª": 4}
    idx = index_map.get(nth, 0)
    actual = context.delays_after[idx]
    assert actual == expected, f"Expected delay {expected}ms at step {nth} but got {actual}ms"


@then('a chamada falha com "{message}"')
def step_assert_call_fails(context, message):
    assert context.call_exception is not None, "Expected exception but call succeeded"
    assert message in str(context.call_exception), \
        f"Expected '{message}' but got '{context.call_exception}'"


@then('o delay foi resetado para o valor base')
def step_assert_delay_reset(context):
    # After a successful call with reset, the delay will have been doubled from baseline
    # because delayed_function doubles delay after each successful call
    # But the reset happens BEFORE the call, so during the call delay was baseline (20)
    # After the call, delay became baseline * 2 = 40
    assert cb.delay == cb.baseline * 2, \
        f"Expected delay {cb.baseline * 2} (baseline doubled after call) but got {cb.delay}"
