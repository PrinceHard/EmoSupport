Feature: reconhecimento de pacientes 

    Scenario: um paciente deve ser reconhecido entre os visitantes
        Given o ambiente de reconhecimento seja configurado com sucesso
        When a foto ./faces/visitantes1.jpg de visitantes for capturada
        Then pelo menos, um(a) paciente deve ser reconhecido(a)
        Then pelo menos, um(a) paciente deve iniciar sessao 

    Scenario: nao deve reconhecer nenhum paciente entre os visitantes 
        Given o ambiente de reconhecimento seja configurado com sucesso
        When a foto ./faces/visitantes3.jpg de visitantes for capturada
        Then nenhum(a) paciente deve ser reconhecido(a)

    Scenario Outline: reconhecer pacientes de varias fotos de visitantes  
        Given o ambiente de reconhecimento seja configurado com sucesso
        When a foto <foto_capturada> de visitantes for capturada
        Then <total_de_reconhecidos> pacientes devem ser reconhecidos

        Examples:
            | foto_capturada          | total_de_reconhecidos    |
            | ./faces/visitantes1.jpg | 1                        |
            | ./faces/visitantes2.jpg | 0                        |
            | ./faces/visitantes3.jpg | 0                        |
            | ./faces/visitantes4.jpg | 1                        |
            | ./faces/visitantes5.jpg | 2                        |
