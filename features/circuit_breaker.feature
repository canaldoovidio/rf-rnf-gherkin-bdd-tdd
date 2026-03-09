# language: pt

Funcionalidade: Circuit Breaker para Integração Externa
  Como um sistema que depende de serviços externos
  Quero que o circuit breaker proteja contra sobrecarga
  Para garantir resiliência quando serviços externos falham

  Cenário: Circuito permanece fechado quando serviço responde normalmente
    Dado que o circuit breaker está no estado "closed"
    E o serviço externo responde em menos de 1000ms
    Quando uma chamada é feita ao serviço externo
    Então a resposta é recebida com sucesso
    E o circuit breaker permanece no estado "closed"

  Cenário: Circuito abre quando serviço falha
    Dado que o circuit breaker está no estado "closed"
    E o serviço externo está falhando com delay acima de 1000ms
    Quando uma chamada é feita ao serviço externo
    Então a chamada falha com exceção
    E o circuit breaker muda para o estado "open"

  Cenário: Circuito rejeita chamadas quando está aberto
    Dado que o circuit breaker está no estado "open"
    E o tempo de abertura ainda não expirou
    Quando uma chamada é feita ao serviço externo
    Então a chamada é rejeitada imediatamente com "Circuit is OPEN"
    E o serviço externo não é chamado

  Cenário: Circuito recupera após timeout com chamada bem-sucedida
    Dado que o circuit breaker está no estado "open"
    E já se passaram mais de 3 segundos desde a abertura
    Quando uma chamada é feita ao serviço externo
    Então a resposta é recebida com sucesso
    E o circuit breaker muda para o estado "closed"

  Cenário: Circuito fecha após recuperação bem-sucedida
    Dado que o circuit breaker está no estado "half-open"
    E o serviço externo voltou a responder normalmente
    Quando uma chamada de teste é feita ao serviço externo
    Então a resposta é recebida com sucesso
    E o circuit breaker muda para o estado "closed"
