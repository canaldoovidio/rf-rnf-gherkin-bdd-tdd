# RF/RNF como Código — BDD, Gherkin e Táticas de Robustez

Projeto de referência para a disciplina **Engenharia de Software (ES09)** turma 13 do Inteli. Demonstra como aferir requisitos funcionais e não funcionais usando BDD (Behavior-Driven Development), testes unitários e testes de carga.

## Stack

- **Python 3.10+**
- **Flask** — API REST com endpoints de demonstração
- **Behave** — BDD com Gherkin em português
- **pytest** — Testes unitários com MagicMock
- **Locust** — Testes de carga e performance

## Estrutura de Diretórios

```
rf-rnf-gherkin-bdd-tdd/
├── app.py                              # Flask app — endpoints /retry-example, /circuit-breaker-example
├── requirements.txt                    # Dependências do projeto
├── features/                           # BDD com Behave (Gherkin em PT-BR)
│   ├── detect_deviation.feature        # Feature: Detecção de Desvio de Rota
│   ├── circuit_breaker.feature         # Feature: Circuit Breaker (CLOSED/OPEN/HALF-OPEN)
│   ├── retry_resilience.feature        # Feature: Retry com resiliência
│   └── steps/
│       ├── detect_deviation_steps.py   # Steps para detecção de desvio
│       ├── circuit_breaker_steps.py    # Steps para circuit breaker
│       └── retry_resilience_steps.py   # Steps para retry
├── src/services/                       # Lógica de negócio
│   ├── deviation_analyzer.py           # Análise de desvio de rota (consome RouteOptimizer)
│   ├── route_optimizer.py              # Cálculo de rotas alternativas
│   ├── distance_calculator.py          # Fórmula de Haversine — distância entre coordenadas GPS
│   └── retry_circuit_breaker.py        # Circuit Breaker com estados CLOSED/OPEN/HALF-OPEN
└── tests/
    ├── unit/                           # Testes unitários
    │   ├── test_deviation_analyzer.py  # Testes do DeviationAnalyzer com MagicMock
    │   └── test_distance_calculator.py # Testes do DistanceCalculator
    ├── integration/                    # Testes de integração entre services
    │   └── test_integration_services.py
    └── carga/
        └── locustfile.py               # Teste de carga com Locust
```

## Como Instalar

```bash
# 1. Clonar o repositório
git clone https://github.com/canaldoovidio/rf-rnf-gherkin-bdd-tdd.git
cd rf-rnf-gherkin-bdd-tdd

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependências
pip install flask behave pytest locust
```

## Como Rodar

### BDD com Behave (Gherkin)

```bash
# Rodar todos os testes BDD
behave

# Rodar uma feature específica
behave features/detect_deviation.feature
behave features/circuit_breaker.feature
behave features/retry_resilience.feature
```

### Testes Unitários com pytest

```bash
# Rodar todos os testes
pytest

# Rodar apenas testes unitários
pytest tests/unit/ -v

# Rodar apenas testes de integração
pytest tests/integration/ -v
```

### Flask (API)

```bash
# Iniciar o servidor
python app.py

# Endpoints disponíveis:
# GET /retry-example          — Demonstra retry com delay crescente
# GET /circuit-breaker-example — Demonstra circuit breaker (CLOSED/OPEN/HALF-OPEN)
# GET /test-page              — Página HTML para testar retry visualmente
# GET /test-circuit-breaker   — Página HTML para testar circuit breaker visualmente
```

### Teste de Carga com Locust

```bash
# 1. Em um terminal, iniciar o Flask
python app.py

# 2. Em outro terminal, iniciar o Locust
locust -f tests/carga/locustfile.py --host=http://localhost:5000

# 3. Abrir http://localhost:8089 no browser
# Configurar: Number of users = 50, Spawn rate = 10

# Modo headless (CI/CD):
locust -f tests/carga/locustfile.py --host=http://localhost:5000 \
    --headless -u 50 -r 10 --run-time 30s --csv=results
```

## Conceitos Demonstrados

| Conceito | Arquivo | Descrição |
|----------|---------|-----------|
| BDD / Gherkin | `features/*.feature` | Cenários em linguagem natural (PT-BR) |
| Injeção de Dependência | `deviation_analyzer.py` | `route_optimizer` injetado no construtor |
| Circuit Breaker | `retry_circuit_breaker.py` | Estados CLOSED → OPEN → HALF-OPEN |
| MagicMock | `tests/unit/test_deviation_analyzer.py` | Isolamento de dependências nos testes |
| Teste de Carga | `tests/carga/locustfile.py` | Simulação de múltiplos usuários |

## Referências

- **Tactics and Patterns for Software Robustness** — Artigo base sobre táticas de robustez
- **SEI/CMU Integrability (Kazman et al., 2020)** — Táticas de integrabilidade
- **ISO/IEC 25010** — Modelo de qualidade de produto de software
