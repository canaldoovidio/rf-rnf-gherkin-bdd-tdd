from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 2)  # Tempo de espera entre as tarefas (em segundos)

    @task(2)
    def test_retry_example(self):
        # Realiza um GET no endpoint /retry-example
        with self.client.get("/retry-example", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status code: {response.status_code}")
            else:
                response.success()

    @task(1)
    def test_circuit_breaker_example(self):
        # Realiza um GET no endpoint /circuit-breaker-example
        with self.client.get("/circuit-breaker-example", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Unexpected status code: {response.status_code}")
            else:
                response.success()
