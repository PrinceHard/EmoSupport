Feature: verificando se o paciente precisa de encaminhamento profissional

    Scenario: um paciente reconhecido pode precisar de encaminhamento profissional 
        Given o ambiente de reconhecimento seja configurado com sucesso
        When a foto ./faces/visitantes1.jpg de visitantes for capturada
        Then pelo menos, um(a) paciente deve ser reconhecido(a)
        Then pelo menos, um(a) paciente deve iniciar sessao
        When a probabilidade de apresentar sinal de angustia ou desespero for 0 porcento
        When a pontuacao detectada do paciente precisar de encaminhamento profissional for 10
        Then pelo menos, um(a) paciente deve ser encaminhado para um profissional

    Scenario: um paciente reconhecido nao precisa de encaminhamento profissional
        Given o ambiente de reconhecimento seja configurado com sucesso
        When a foto ./faces/visitantes1.jpg de visitantes for capturada
        Then pelo menos, um(a) paciente deve ser reconhecido(a)
        Then pelo menos, um(a) paciente deve iniciar sessao
        When a probabilidade de apresentar sinal de angustia ou desespero for 0 porcento
        When a pontuacao detectada do paciente precisar de encaminhamento profissional for 0
        Then nenhum paciente deve ser encaminhado para um profissional
