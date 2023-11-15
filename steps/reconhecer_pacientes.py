from behave import given, when, then
from service import *

@given("o ambiente de reconhecimento seja configurado com sucesso")
def given_ambiente_configurado_com_sucesso(context):
    configurado, context.configuracao = preparar()

    assert configurado 

@when("a foto {foto} de visitantes for capturada")
def when_foto_de_visitantes_capturada(context, foto):
    context.visitantes = simular_visitas(foto)

    assert context.visitantes is not None

@then("pelo menos, um(a) paciente deve ser reconhecido(a)")
def then_um_paciente_reconhecido(context):
    pacientes_reconhecidos, context.pacientes = reconhecer_pacientes(context.configuracao, context.visitantes)

    assert pacientes_reconhecidos

@then("pelo menos, um(a) paciente deve iniciar sessao")
def then_um_paciente_atendido(context):
    tem_paciente_em_sessao, context.pacientes_em_sessao = receber_pacientes(context.pacientes)

    assert tem_paciente_em_sessao

@then("nenhum(a) paciente deve ser reconhecido(a)")
def then_nenhum_paciente_reconhecido(context):
    pacientes_reconhecidos, context.pacientes = reconhecer_pacientes(context.configuracao, context.visitantes)

    assert not pacientes_reconhecidos 

@then("{total_de_reconhecimentos} pacientes devem ser reconhecidos")
def then_total_de_pacientes_reconhecidos(context, total_de_reconhecimentos):
    _, context.pacientes = reconhecer_pacientes(context.configuracao, context.visitantes)

    assert len(context.pacientes) == int(total_de_reconhecimentos)
