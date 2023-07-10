import socket
import threading


class ServerConfig:
    HOST = '127.0.0.1'  # Endereço IP do servidor
    PORTA = 9001  # Porta para conexão


def exibir_opcoes_votacao():
    print('Opções de votação:')
    print('1. Votar a favor da inelegibilidade do ex-presidente')
    print('2. Votar contra a inelegibilidade do ex-presidente')


def iniciar_thread_acompanhamento(escolha):
    thread = threading.Thread(target=receber_atualizacoes, args=(escolha,))
    thread.start()
    thread.join()  # Aguarda até que a thread de atualizações seja concluída


def conectar_servidor(funcao):
    def funcao_interna(escolha):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((ServerConfig.HOST, ServerConfig.PORTA))
            client_socket.sendall(escolha.encode())
            return funcao(client_socket)

    return funcao_interna


@conectar_servidor
def votar(client_socket):
    votacao_encerrada = client_socket.recv(1024).decode()

    if votacao_encerrada == '0':
        exibir_opcoes_votacao()
        opcao = input('Digite o número da opção desejada: ')
        client_socket.sendall(opcao.encode())

        resposta = client_socket.recv(1024).decode()
        print(resposta)
        return msg_final(resposta)
    else:
        resposta = client_socket.recv(1024).decode()
        print(resposta)
        return msg_final(resposta)


@conectar_servidor
def receber_atualizacoes(client_socket):
    while True:
        resposta = client_socket.recv(1024).decode()
        print(resposta)
        if msg_final(resposta):
            break


def msg_final(msg):
    return msg.startswith('Votação encerrada:')


def executar_cliente():
    while True:
        print('--- MENU ---')
        print('1. Votar')
        print('2. Acompanhar votação')

        escolha = input('Escolha uma opção: ')
        if escolha == '1':
            votacao_encerrada = votar(escolha)  # Sem passar a escolha como argumento
            if votacao_encerrada:
                break

        elif escolha == '2':
            iniciar_thread_acompanhamento(escolha)
            break

        else:
            print('Opção inválida!')

        acompanhar_votacao = input('Deseja acompanhar a votação? (S/N): ')
        if acompanhar_votacao.lower() == 's':
            iniciar_thread_acompanhamento('2')
            break
        else:
            break


if __name__ == '__main__':
    executar_cliente()
