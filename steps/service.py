import face_recognition as reconhecedor
import simpy
import json
import secrets
import colored
import random
import time
from datetime import datetime

ARQUIVO_DE_CONFIGURACAO = "./config.json"

TEMPO_DE_DETECCAO_DE_PACIENTES = 40
TEMPO_DE_SIMULACAO = 1000
PROBABILIDADE_ANGUSTIA_DESESPERO = 10 

def preparar():
    configurado, configuracao = False, None
    try:
        with open(ARQUIVO_DE_CONFIGURACAO, "r") as arquivo:
            configuracao = json.load(arquivo)
            if configuracao:
                print("Arquivo de configuração carregado")
            arquivo.close()

            configurado = True
    except Exception as e:
        print(f"Erro lendo configuração: {str(e)}")

    return configurado, configuracao

def simular_visitas(foto):
    print(f"foto de visitantes: {foto}")

    visitantes = {
        "foto": foto,
        "hackers": None
    }

    return visitantes

def reconhecer_pacientes(configuracao, visitantes):
    foto_visitantes = reconhecedor.load_image_file(visitantes["foto"])
    caracteristicas_dos_visitantes = reconhecedor.face_encodings(foto_visitantes)

    pacientes = []
    for paciente in configuracao["pacientes"]:
        fotos = paciente["fotos"]
        total_de_reconhecimentos = 0

        for foto in fotos:
            foto_paciente = reconhecedor.load_image_file(foto)
            caracteristicas_paciente = reconhecedor.face_encodings(foto_paciente)[0]

            reconhecimentos = reconhecedor.compare_faces(caracteristicas_dos_visitantes, caracteristicas_paciente)
            if True in reconhecimentos:
                total_de_reconhecimentos += 1

        if total_de_reconhecimentos/ len(fotos) >= 0.6:
            pacientes.append(paciente)

    return len(pacientes) > 0, pacientes

def receber_pacientes(pacientes_reconhecidos):
    pacientes_em_sessao = {}

    for paciente in pacientes_reconhecidos:

        id_sessao = secrets.token_hex(nbytes=16).upper()
        pacientes_em_sessao[id_sessao] = paciente

        imprimir_dados_do_paciente(paciente)

    return len(pacientes_em_sessao) > 0, pacientes_em_sessao

def oferecer_suporte_emocional(paciente):
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

def detectar_sinais_de_angustia_e_desespero(probabilidade_de_angustia_ou_desespero):
    emocao_detectada = random.randint(1, 100) <= probabilidade_de_angustia_ou_desespero

    return emocao_detectada

def avaliar_encaminhamento_profissional(avaliacao_minima, pontuacao_detectada):
    encaminhado = False

    if pontuacao_detectada >= avaliacao_minima:
        encaminhado = encaminhar_para_profissional()
        return encaminhado
    else:
        return encaminhado

def encaminhar_para_profissional():
        return True

def imprimir_dados_do_paciente(paciente):
    print(colored.fg('black'), colored.bg('grey_54'), f"Paciente reconhecido em {datetime.now()} dentre os visitantes", 
          colored.attr('reset'))
    print(colored.fg('black'), colored.bg('white'), f"Nome {paciente['nome']}", colored.attr('reset')) 
    print(colored.fg('black'), colored.bg('white'), f"Idade {paciente['idade']}", colored.attr('reset')) 
    print(colored.fg('black'), colored.bg('white'), f"Endereço {paciente['endereco']}", colored.attr('reset')) 

