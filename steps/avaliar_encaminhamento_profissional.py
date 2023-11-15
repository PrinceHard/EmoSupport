from behave import when, then
from service import *

@when("a pontuacao detectada do paciente precisar de encaminhamento profissional for {pontuacao_detectada}")
def when_tiver_pontuacao_detectada_paciente_precisar_encaminhamento_profissional_maior_avaliacao_minima(context, pontuacao_detectada):
    avaliacao_minima = 5
    context.encaminhado = avaliar_encaminhamento_profissional(avaliacao_minima, int(pontuacao_detectada))

@then("pelo menos, um(a) paciente deve ser encaminhado para um profissional")
def then_paciente_encaminhado_profissional(context):
    assert context.encaminhado

@then("nenhum paciente deve ser encaminhado para um profissional")
def then_nenhum_paciente_encaminhado_profissional(context):
    assert not context.encaminhado
