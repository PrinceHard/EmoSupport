import face_recognition as reconhecedor
import simpy
import json
import secrets
import colored
import random
import time
from datetime import datetime

FOTOS_VISITANTES = [
    "./faces/visitantes1.jpg",
    "./faces/visitantes2.jpg"
]
ARQUIVO_DE_CONFIGURACAO = "config.json"

TEMPO_DE_DETECCAO_DE_PACIENTES = 40
TEMPO_DE_SIMULACAO = 1000
PROBABILIDADE_ANGUSTIA_DESESPERO = 0.4

def preparar():
    global configuracao

    configuracao = None
    try:
        with open(ARQUIVO_DE_CONFIGURACAO, "r") as arquivo:
            configuracao = json.load(arquivo)
            if configuracao:
                print("Arquivo de configuração carregado")
    except Exception as e:
        print(f"Erro lendo configuração: {str(e)}")

    global pacientes_reconhecidos
    pacientes_reconhecidos = {}


def simular_visitas():
    if not FOTOS_VISITANTES:
        print("A lista de fotos de visitantes está vazia.")
        return None

    foto = random.choice(FOTOS_VISITANTES)
    print(f"Foto de visitantes: {foto}")

    visitantes = {
        "foto": foto,
        "pacientes": None
    }

    return visitantes

def paciente_reconhecido_anteriormente(paciente):
    global pacientes_reconhecidos

    reconhecido_previamente = False
    for reconhecido in pacientes_reconhecidos.values():
        if paciente["id"] == reconhecido["id"]:
            reconhecido_previamente = True

            break

    return reconhecido_previamente

def reconhecer_pacientes(visitantes):
    global configuracao

    print("Realizando reconhecimento de pacientes...")
    foto_visitantes = reconhecedor.load_image_file(visitantes["foto"])
    caracteristicas_dos_visitantes = reconhecedor.face_encodings(
        foto_visitantes)

    pacientes = []
    for paciente in configuracao["pacientes"]:
        fotos = paciente["fotos"]
        for foto in fotos:
            foto_paciente = reconhecedor.load_image_file(foto)
            caracteristicas_paciente = reconhecedor.face_encodings(foto_paciente)[0]

            reconhecimentos = reconhecedor.compare_faces(
                caracteristicas_dos_visitantes, caracteristicas_paciente)
            if True in reconhecimentos:
                pacientes.append(paciente)
                pacientes_reconhecidos[paciente["id"]] = paciente
                break

    if len(pacientes) > 0:
        return True, pacientes
    else:
        print(colored.fg('black'), colored.bg('yellow'), "Nenhum paciente reconhecido dentre os visitantes", 
              colored.attr('reset'))
        return False, None


def oferecer_suporte_emocional(paciente):
    print(colored.fg('black'), colored.bg('blue'), f"Oferecendo suporte emocional personalizado para o(a) :{paciente['nome']}", 
          colored.attr('reset'))

    while True:
        if not detectar_sinais_de_angustia_e_desespero(paciente):

            if avaliar_encaminhamento_profissional(paciente):
                break

            # Simulando uma lista de necessidades emocionais do paciente
            necessidades_emocionais = ["Motivação", "Calma", "Felicidade", "Conforto"]
            
            # Sorteando uma necessidade emocional aleatória
            necessidade_simulada = random.choice(necessidades_emocionais)

            print(colored.fg('black'), colored.bg('white'), f"Necessidade emocional: {necessidade_simulada}", colored.attr('reset'))

            # Lógica para oferecer suporte emocional com base na necessidade emocional sorteada
            if necessidade_simulada == "Motivação":
                print(colored.fg('black'), colored.bg('white'), "Frases motivacionais:")
                frase = paciente["suporte_emocional"]["motivacao"]
                print(colored.fg('black'), colored.bg('white'), f"- {frase}", colored.attr('reset'))
            elif necessidade_simulada == "Calma":
                print(colored.fg('black'), colored.bg('white'), "Atividades para acalmar:")
                atividade = paciente["suporte_emocional"]["calma"]
                print(colored.fg('black'), colored.bg('white'), f"- {atividade}", colored.attr('reset'))
            elif necessidade_simulada == "Felicidade":
                print(colored.fg('black'), colored.bg('white'), "Atividades para se sentir Feliz:")
                atividade = paciente["suporte_emocional"]["felicidade"]
                print(colored.fg('black'), colored.bg('white'), f"- {atividade}", colored.attr('reset'))
            elif necessidade_simulada == "Conforto":
                print(colored.fg('black'), colored.bg('white'), "Atividades Confortantes:")
                atividade = paciente["suporte_emocional"]["conforto"]
                print(colored.fg('black'), colored.bg('white'), f"- {atividade}", colored.attr('reset'))
        else:
            print("Angústia ou desespero detectado. O suporte emocional foi interrompido.")
            break 

        time.sleep(5)


def detectar_sinais_de_angustia_e_desespero(paciente):
    emocao_detectada = random.random() < PROBABILIDADE_ANGUSTIA_DESESPERO

    if emocao_detectada:
        print(colored.fg('black'), colored.bg('red'), f"Expressão de angústia ou desespero detectada no(a) paciente {paciente['nome']}",
              colored.attr('reset'))
        print(colored.fg('black'), colored.bg('red'), "Ligando para a emergência...", colored.attr('reset'))
        print(colored.fg('black'), colored.bg('red'), f"Enviando um socorro para o endereço: {paciente['endereco']}.",
              colored.attr('reset'))
        return True
    else:
        print(colored.fg('white'), colored.bg('green'), "Nenhuma expressão de angústia ou desespero foi detectada.")
        return False

def avaliar_encaminhamento_profissional(paciente):
    avaliacao_minima = paciente["encaminhamento_profissional"]["avaliacao_minima"]

    pontuacao_atual = random.randint(1, 10)

    if pontuacao_atual >= avaliacao_minima:
        print(colored.fg('black'), colored.bg('yellow'), f"{paciente['nome']} demonstrou emoções mais sensíveis.",
              colored.attr('reset'))
        print(colored.fg('black'), colored.bg('yellow'), f"Paciente {paciente['nome']} precisa de encaminhamento para ajuda profissional.",
              colored.attr('reset'))
        paciente["encaminhamento_profissional"]["historico_suporte"].append(
                {"data": datetime.now(), "avaliacao": pontuacao_atual, "encaminhado": True}
                )
        return encaminhar_para_profissional(paciente)
    else:
        print(colored.fg('white'), colored.bg('green'), f"Paciente {paciente['nome']} não precisa de encaminhamento para ajuda profissional no momento.",
              colored.attr('reset'))
        paciente["encaminhamento_profissional"]["historico_suporte"].append(
                {"data": datetime.now(), "avaliacao": pontuacao_atual, "encaminhado": False}
                )
        return False

def encaminhar_para_profissional(paciente):
        print(colored.fg('black'), colored.bg('yellow'), "Encaminhando...", colored.attr('reset'))
        print(colored.fg('black'), colored.bg('yellow'), "Notificando a equipe de apoio...", colored.attr('reset'))
        print(colored.fg('black'), colored.bg('white'), f"{paciente['nome']} foi encaminhado para ajuda profissional.", colored.attr('reset'))
        return True

def imprimir_dados_do_paciente(paciente):
    print(colored.fg('black'), colored.bg('grey_54'), f"Paciente reconhecido em {datetime.now()} dentre os visitantes", 
          colored.attr('reset'))
    print(colored.fg('black'), colored.bg('white'), f"Nome {paciente['nome']}", colored.attr('reset')) 
    print(colored.fg('black'), colored.bg('white'), f"Idade {paciente['idade']}", colored.attr('reset')) 
    print(colored.fg('black'), colored.bg('white'), f"Endereço {paciente['endereco']}", colored.attr('reset')) 
    oferecer_suporte_emocional(paciente)

def reconhecer_visitantes(ambiente_de_simulacao):
    global pacientes_reconhecidos

    while ambiente_de_simulacao.now - ambiente_de_simulacao.now < TEMPO_DE_SIMULACAO:
        print(
            f"Reconhecendo pacientes entre visitantes...")

        visitantes = simular_visitas()
        ocorreram_reconhecimentos, pacientes = reconhecer_pacientes(visitantes)
        if ocorreram_reconhecimentos:
            for paciente in pacientes:

                id_sessao = secrets.token_hex(nbytes=16).upper()
                pacientes_reconhecidos[id_sessao] = paciente
                imprimir_dados_do_paciente(paciente)

        yield ambiente_de_simulacao.timeout(TEMPO_DE_DETECCAO_DE_PACIENTES)

if __name__ == "__main__":
    preparar()

    ambiente_de_simulacao = simpy.Environment()
    ambiente_de_simulacao.process(reconhecer_visitantes(ambiente_de_simulacao))
    ambiente_de_simulacao.run(until=500)
