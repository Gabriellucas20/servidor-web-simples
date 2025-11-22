# Importa o módulo socket
from socket import *
import sys # Necessário para encerrar o programa

# Cria o socket TCP (orientado à conexão)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepara o socket do servidor
#Fill in start
serverPort = 6789 # Define a porta de escuta
serverSocket.bind(('', serverPort)) # Associa o socket ao endereço e porta
serverSocket.listen(1) # Começa a escutar por conexões, com no máximo 1 conexão pendente
#Fill in end

while True:
    # Estabelece a conexão
    print('Ready to serve...')
    #Fill in start
    connectionSocket, addr = serverSocket.accept() # Aceita a conexão e recebe o novo socket e o endereço do cliente
    #Fill in end

    try:
        # Recebe a mensagem do cliente (requisição HTTP)
        #Fill in start
        message = connectionSocket.recv(1024).decode() # Recebe até 1024 bytes e decodifica para string
        #Fill in end

        # Analisa a requisição para determinar o nome do arquivo
        filename = message.split()[1] # O nome do arquivo é o segundo elemento (índice 1) do cabeçalho
        
        # Abre o arquivo (o [1:] remove a barra inicial '/')
        f = open(filename[1:])
        
        # Lê todo o conteúdo do arquivo
        outputdata = f.read() 
        #Fill in start # Preenche o conteúdo do arquivo
        #Fill in end
        
        # Envia a linha de status do cabeçalho HTTP
        #Fill in start
        connectionSocket.send('HTTP/1.1 200 OK\r\n'.encode()) # Envia a linha de status 200 OK
        # Envia um cabeçalho Content-Type
        connectionSocket.send('Content-Type: text/html\r\n\r\n'.encode()) # Inclui uma linha em branco final para o fim dos cabeçalhos
        #Fill in end

        # Envia o conteúdo do arquivo ao cliente
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send(('\r\n').encode())

        # Fecha a conexão com o cliente
        connectionSocket.close()

    except IOError:
        # Envia mensagem de erro 404 se o arquivo não for encontrado
        #Fill in start
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n'.encode()) # Envia a linha de status 404 Not Found
        connectionSocket.send('Content-Type: text/html\r\n\r\n'.encode())
        connectionSocket.send('<html><head><title>404 Not Found</title></head>'.encode())
        connectionSocket.send('<body><h1>404 Not Found</h1>'.encode())
        connectionSocket.send('<p>O arquivo solicitado não foi encontrado no servidor.</p></body></html>\r\n'.encode())
        #Fill in end

        # Fecha o socket do cliente
        #Fill in start
        connectionSocket.close()
        #Fill in end

serverSocket.close()
sys.exit() # Encerra o programa