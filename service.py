import face_recognition as reconhecedor
import simpy
import json
import secrets
import colored
import random
from datetime import datetime

FOTOS_VISITANTES = [
    "./faces/visitantes1.jpg",
    "./faces/visitantes2.jpg"
]
ARQUIVO_DE_CONFIGURACAO = "config.json"

TEMPO_DE_DETECCAO_DE_PACIENTES = 40
TEMPO_DE_SIMULACAO = 1000

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
        print(colored.fg('black'), colored.bg('red'), "Nenhum paciente reconhecido dentre os visitantes", 
              colored.attr('reset'))
        return False, None


def oferecer_suporte_emocional(paciente):
    print(colored.fg('black'), colored.bg('green'), f"Oferecendo suporte emocional personalizado para o(a) :{paciente['nome']}", 
          colored.attr('reset'))

    # Simulando uma lista de necessidades emocionais do paciente
    necessidades_emocionais = ["Motivação", "Calma", "Felicidade", "Conforto"]
    
    # Sorteando uma necessidade emocional aleatória
    necessidade_simuladas = random.choice(necessidades_emocionais)

    print(colored.fg('black'), colored.bg('white'), f"Necessidade emocional: {necessidade_aleatoria}", colored.attr('reset'))

    # Lógica para oferecer suporte emocional com base na necessidade emocional sorteada
    if necessidade_simuladas == "Motivação":
        print(colored.fg('black'), colored.bg('white'), "Frases motivacionais:")
        for frase in paciente["suporte_emocional"]["atividades_motivacionais"]:
            print(colored.fg('black'), colored.bg('white'), f"- {frase}", colored.attr('reset'))
    elif necessidade_aleatoria == "Calma":
        print(colored.fg('black'), colored.bg('white'), "Atividades para acalmar:")
        for atividade in paciente["suporte_emocional"]["atividades_motivacionais"]:
            print(colored.fg('black'), colored.bg('white'), f"- {atividade}", colored.attr('reset'))

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
    ambiente_de_simulacao.run(until=1000)
