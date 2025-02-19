import time
import asyncio

# Estados possíveis
CLOSED = "closed"
OPEN = "open"
HALF_OPEN = "half-open"

circuit_state = CLOSED
time_opened = 0
open_duration = 3    # <--- reduzido para 3 segundos
test_in_half_open = False

# Controle de falhas (simulando delay crescente)
baseline = 20
delay = baseline
time_error_occurred = None

async def circuit_breaker_function():
    """
    Simula um Circuit Breaker com CLOSED, OPEN e HALF_OPEN.
    """
    global circuit_state, time_opened, test_in_half_open

    current_time = time.time()

    # Se está OPEN, verifica se o tempo já expirou
    if circuit_state == OPEN:
        if (current_time - time_opened) >= open_duration:
            # Passa para HALF_OPEN e permite 1 tentativa de teste
            circuit_state = HALF_OPEN
            test_in_half_open = False
        else:
            raise Exception("Circuit is OPEN")

    # Se estamos em HALF_OPEN, permitimos somente 1 chamada de teste
    if circuit_state == HALF_OPEN:
        if test_in_half_open:
            raise Exception("Circuit is HALF_OPEN - waiting for next cycle")
        test_in_half_open = True

    # Tenta executar a função real
    try:
        result = await delayed_function()
    except Exception as e:
        # Se falhar, abre o circuito
        circuit_state = OPEN
        time_opened = time.time()
        raise e

    # Se funcionou e estávamos em HALF_OPEN, fecha o circuito
    if circuit_state == HALF_OPEN:
        circuit_state = CLOSED

    return {
        "message": result,
        "circuit_state": circuit_state
    }

async def delayed_function():
    """
    Simula falha quando o delay excede 1000ms.
    Reseta o delay após 5s sem chamadas bem-sucedidas.
    """
    global baseline, delay, time_error_occurred

    current_time = time.time() * 1000
    if time_error_occurred:
        if (current_time - time_error_occurred) > 5000:
            delay = baseline
            time_error_occurred = None

    if delay > 1000:
        time_error_occurred = current_time
        raise Exception("Service failing")

    await asyncio.sleep(delay / 1000)
    msg = f"Service is responding in {delay} ms"
    delay *= 2
    return msg
