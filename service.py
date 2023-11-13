import face_recognition
import cv2
import json

def carregar_configuracao():
    # Carregar configurações a partir do arquivo JSON
    with open('config.json') as f:
        configuracao = json.load(f)
    return configuracao

def reconhecimento_facial(configuracao):
    # Carregar imagens de usuários estáticos
    imagens_usuarios = []
    for usuario in configuracao['usuarios']:
        imagem_usuario = face_recognition.load_image_file(usuario['caminho_imagem'])
        imagens_usuarios.append(imagem_usuario)

    # Criar perfis de usuários
    perfis_usuarios = []
    for i, imagem_usuario in enumerate(imagens_usuarios):
        face_codificacao = face_recognition.face_encodings(imagem_usuario)[0]
        perfil_usuario = {'id': i+1, 'nome': configuracao['usuarios'][i]['nome'], 'codificacao': face_codificacao}
        perfis_usuarios.append(perfil_usuario)

    # Iniciar captura de vídeo
    cap = cv2.VideoCapture(0)

    while True:
        # Capturar um quadro do vídeo
        ret, frame = cap.read()

        # Identificar faces no quadro
        faces = face_recognition.face_locations(frame)

        if faces:
            codificacoes_faces = face_recognition.face_encodings(frame, faces)

            for face_codificacao in codificacoes_faces:
                # Comparar com as codificações de usuários
                matches = face_recognition.compare_faces([perfil['codificacao'] for perfil in perfis_usuarios], face_codificacao)

                nome_usuario = "Desconhecido"
                if True in matches:
                    indice_match = matches.index(True)
                    nome_usuario = perfis_usuarios[indice_match]['nome']

                # Desenhar retângulo e nome na face identificada
                top, right, bottom, left = faces[0]  # Usaremos a primeira face encontrada
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, nome_usuario, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Exibir o quadro resultante
        cv2.imshow('Reconhecimento Facial', frame)

        # Encerrar o programa ao pressionar 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Carregar configurações
    configuracao = carregar_configuracao()

    # Iniciar processo de reconhecimento facial
    reconhecimento_facial(configuracao)

