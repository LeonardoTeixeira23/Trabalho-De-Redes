import socket
import threading


# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORTA = 9001  # Porta para conexão

# Opções de votação
opcoes = {
    '1': 'A favor',
    '2': 'Contra'
}

# Contagem dos votos
votos = {
    '1': 5,
    '2': 0
}

# Lista de clientes conectados
clientes = []


def exibir_resultado():
    resultado = f'[{votos["1"]}] A favor, [{votos["2"]}] Contra'

    if sum(votos.values()) >= 7:
        mensagem = f'Votação encerrada:\nResultado final: {resultado}'
    else:
        mensagem = f'Resultado Atual: {resultado}'

    for cliente in clientes:
        cliente.sendall(mensagem.encode())


def processar_voto(conn):
    voto = conn.recv(1024).decode().strip()
    if voto in opcoes:
        votos[voto] += 1
        exibir_resultado()
    else:
        conn.sendall('Opção de voto inválida!\n'.encode())


def lidar_com_cliente(conn, addr):
    print('Cliente conectado:', addr)
    clientes.append(conn)

    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break

        if data == '1':
            if sum(votos.values()) >= 7:
                conn.sendall('1'.encode())
                exibir_resultado()
            else:
                conn.sendall('0'.encode())
                processar_voto(conn)
        elif data == '2':
            while sum(votos.values()) < 7:
                new_data = conn.recv(1024).decode().strip()
                if not new_data:
                    break
                exibir_resultado()
        else:
            conn.sendall('Opção inválida!\n'.encode())

    clientes.remove(conn)
    conn.close()
    print('Cliente desconectado:', addr)


def executar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_servidor:
        socket_servidor.bind((HOST, PORTA))
        socket_servidor.listen()

        print('Servidor pronto para receber conexões...')

        while True:
            conn, addr = socket_servidor.accept()
            thread = threading.Thread(target=lidar_com_cliente, args=(conn, addr))
            thread.start()


if __name__ == '__main__':
    executar_servidor()
