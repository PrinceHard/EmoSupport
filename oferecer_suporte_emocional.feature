Feature: oferecendo suporte emocional ao paciente 

    Scenario: um paciente deve se 
        Given o ambiente de reconhecimento seja preparado com sucesso
        When a foto ./faces/personagens2.jpg de visitantes for capturada
        Then pelo menos, um(a) hacker deve ser reconhecido(a)
        Then pelo menos, um(a) hacker deve iniciar sessao
        When a probabilidade de sessao de urgencia for 100 porcento
        Then pelo menos, um(a) hacker deve ser levado(a) para a Reunião

    Scenario: nenhum hacker reconhecido deve ir para a Reunião
        Given o ambiente de reconhecimento seja preparado com sucesso
        When a foto ./faces/personagens2.jpg de visitantes for capturada
        Then pelo menos, um(a) hacker deve ser reconhecido(a)
        Then pelo menos, um(a) hacker deve iniciar sessao
        When a probabilidade de sessao de urgencia for 0 porcento
        Then nenhum hacker deve ir para a Reunião
