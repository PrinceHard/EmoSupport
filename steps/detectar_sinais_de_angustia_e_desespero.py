from behave import when, then
from service import *

@when("a probabilidade de apresentar sinal de angustia ou desespero for {probabilidade} porcento")
def when_probabilidade_de_apresentar_sinal_angustia_desespero(context, probabilidade):
    context.emocao_detectada = detectar_sinais_de_angustia_e_desespero(int(probabilidade))

@then("se deve ligar para emergencia e enviar o socorro para casa do paciente")
def then_ligar_para_emergencia_e_enviar_socorro(context):

    assert context.emocao_detectada   

@then("nenhum paciente deve receber socorro em casa")
def then_nenhum_paciente_deve_receber_socorro_casa(context):
    assert not context.emocao_detectada
