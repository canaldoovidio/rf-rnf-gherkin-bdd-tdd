# language: pt

Funcionalidade: Retry com Resiliência para Serviço Externo
  Como um sistema que depende de serviços externos instáveis
  Quero que chamadas com falha sejam retentadas automaticamente
  Para garantir disponibilidade mesmo com falhas temporárias

  Cenário: Serviço responde na primeira tentativa
    Dado que o serviço externo está funcionando normalmente com delay de 20ms
    Quando uma chamada é feita via delayed_function
    Então a resposta contém "Service is responding"
    E o delay dobra para a próxima chamada

  Cenário: Delay aumenta exponencialmente a cada chamada
    Dado que o delay inicial é 20ms
    Quando 3 chamadas consecutivas são feitas ao serviço
    Então o delay após a 1ª chamada é 40ms
    E o delay após a 2ª chamada é 80ms
    E o delay após a 3ª chamada é 160ms

  Cenário: Serviço falha quando delay excede 1000ms
    Dado que o delay acumulado excedeu 1000ms
    Quando uma chamada é feita via delayed_function
    Então a chamada falha com "Service failing"

  Cenário: Delay reseta após período sem chamadas
    Dado que o serviço falhou e registrou o tempo do erro
    E que já se passaram mais de 5 segundos desde o erro
    Quando uma nova chamada é feita via delayed_function
    Então o delay foi resetado para o valor base
    E a resposta contém "Service is responding"
