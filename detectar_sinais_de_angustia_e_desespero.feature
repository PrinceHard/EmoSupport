Feature: detectando se um paciente apresenta sinal de angustia ou desespero 

    Scenario: um paciente reconhecido pode apresentar sinais de agunstia ou desespero 
        Given o ambiente de reconhecimento seja configurado com sucesso
        When a foto ./faces/visitantes1.jpg de visitantes for capturada
        Then pelo menos, um(a) paciente deve ser reconhecido(a)
        Then pelo menos, um(a) paciente deve iniciar sessao 
        When a probabilidade de apresentar sinal de angustia ou desespero for 100 porcento
        Then se deve ligar para emergencia e enviar o socorro para casa do paciente

    Scenario: nenhum paciente reconhecido apresentou sinais de agunstia ou desespero
        Given o ambiente de reconhecimento seja configurado com sucesso
        When a foto ./faces/visitantes1.jpg de visitantes for capturada
        Then pelo menos, um(a) paciente deve ser reconhecido(a)
        Then pelo menos, um(a) paciente deve iniciar sessao
        When a probabilidade de apresentar sinal de angustia ou desespero for 0 porcento
        Then nenhum paciente deve receber socorro em casa 

