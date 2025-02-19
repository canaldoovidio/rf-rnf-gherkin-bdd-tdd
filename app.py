from flask import Flask, jsonify, render_template_string
import asyncio
from src.services.retry_circuit_breaker import circuit_breaker_function, delayed_function


app = Flask(__name__)

@app.route("/retry-example", methods=["GET"])
def retry_example():
    """
    Endpoint que chama a função 'delayed_function' para demonstrar o comportamento
    de retry e circuit breaker (ou lógica de delay/falha) no Python.
    """
    try:
        message = asyncio.run(delayed_function())  # Chame sua função que aplica o retry pattern
        return jsonify({"status": "success", "message": message})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route("/test-page", methods=["GET"])
def test_page():
    # Utilizamos render_template_string para simplificar; em projetos maiores use templates separados.
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Teste de Retry/Circuit Breaker</title>
        <style>
            table { border-collapse: collapse; width: 80%; margin: 20px auto; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1 style="text-align:center;">Teste de Endpoint Retry</h1>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Tempo do Request (ms)</th>
                    <th>Status Code</th>
                    <th>Response Body</th>
                </tr>
            </thead>
            <tbody id="results">
            </tbody>
        </table>

        <script>
            async function makeRequest(i) {
                const startTime = Date.now();
                try {
                    const response = await fetch('/retry-example');
                    const status = response.status;
                    const body = await response.json();
                    const endTime = Date.now();
                    const elapsed = endTime - startTime;
                    const row = `<tr>
                        <td>${i}</td>
                        <td>${elapsed}</td>
                        <td>${status}</td>
                        <td>${JSON.stringify(body)}</td>
                    </tr>`;
                    document.getElementById('results').innerHTML += row;
                } catch (error) {
                    const endTime = Date.now();
                    const elapsed = endTime - startTime;
                    const row = `<tr>
                        <td>${i}</td>
                        <td>${elapsed}</td>
                        <td>Error</td>
                        <td>${error.toString()}</td>
                    </tr>`;
                    document.getElementById('results').innerHTML += row;
                }
            }

            async function runRequests() {
                for (let i = 1; i <= 10; i++) {
                    await makeRequest(i);
                }
            }

            window.onload = runRequests;
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

from flask import Flask, jsonify, render_template_string
import asyncio
from src.services.retry_circuit_breaker import circuit_breaker_function

app = Flask(__name__)

@app.route("/circuit-breaker-example", methods=["GET"])
async def circuit_breaker_example():
    try:
        data = await circuit_breaker_function()
        return jsonify({"status": "success", **data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e), "circuit_state": "open"}), 500

@app.route("/test-circuit-breaker", methods=["GET"])
def test_circuit_breaker_page():
    """
    Página HTML que faz várias requisições ao endpoint /circuit-breaker-example,
    exibe o estado do circuito (CLOSED, OPEN, HALF_OPEN), e aguarda o tempo
    de abertura (3s) quando receber 'open'.
    """
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Teste de Circuit Breaker</title>
        <style>
            table { border-collapse: collapse; width: 90%; margin: 20px auto; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1 style="text-align:center;">Teste de Endpoint Circuit Breaker</h1>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Tempo do Request (ms)</th>
                    <th>Status Code</th>
                    <th>Estado do Circuito</th>
                    <th>Response Body</th>
                    <th>Próxima Chamada (ms)</th>
                </tr>
            </thead>
            <tbody id="results"></tbody>
        </table>

        <script>
            let requestCount = 30;        // Vamos fazer 20 requisições
            let openWaitTime = 1000;      // 3 segundos (igual open_duration no backend)
            let currentRequest = 1;

            async function makeRequest(i) {
                const startTime = Date.now();
                let nextCallMs = 0;
                let circuitStateDisplay = "unknown";
                let statusDisplay = "Error";
                let responseBody = "";

                try {
                    const response = await fetch('/circuit-breaker-example');
                    const endTime = Date.now();
                    const elapsed = endTime - startTime;
                    const status = response.status;
                    if (!response.ok) {
                        // Se status não for 2xx, lança exceção manual
                        let errorBody;
                        try {
                            errorBody = await response.json();
                        } catch (jsonErr) {
                            errorBody = { message: "Erro desconhecido" };
                        }
                        throw new Error(`${status} - ${errorBody.message}`);
                    }

                    // Se chegou aqui, é 2xx
                    const endTime2 = Date.now();
                    const elapsed2 = endTime2 - startTime;
                    const body = await response.json();
                    circuitStateDisplay = body.circuit_state || "unknown";
                    statusDisplay = status;
                    responseBody = JSON.stringify(body);

                    addRow(i, elapsed2, statusDisplay, circuitStateDisplay, responseBody, nextCallMs);

                } catch (error) {
                    const endTime = Date.now();
                    const elapsed = endTime - startTime;

                    // Tenta extrair do erro se o estado é OPEN
                    let errorMessage = error.toString();
                    if (errorMessage.includes("500 -")) {
                        circuitStateDisplay = "open";
                        // Se está open, aguardamos 3s para permitir a transição para half-open
                        nextCallMs = openWaitTime * 2;
                    }

                    addRow(i, elapsed, "Error", circuitStateDisplay, errorMessage, nextCallMs);

                    // Se precisamos aguardar, aguardamos
                    if (nextCallMs > 0) {
                        await new Promise(resolve => setTimeout(resolve, nextCallMs));
                    }
                }
            }

            function addRow(i, elapsed, status, circuitState, body, nextCall) {
                const row = `<tr>
                    <td>${i}</td>
                    <td>${elapsed}</td>
                    <td>${status}</td>
                    <td>${circuitState}</td>
                    <td>${body}</td>
                    <td>${nextCall}</td>
                </tr>`;
                document.getElementById('results').innerHTML += row;
            }

            async function runRequests() {
                for (let i = 1; i <= requestCount; i++) {
                    await makeRequest(i);
                }
            }

            window.onload = runRequests;
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_content)

if __name__ == "__main__":
    # Executa a aplicação Flask na porta 5000 (padrão)
    app.run(debug=True, host="0.0.0.0", port=5000)
