#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define PORT 8080

int main(int argc, char const* argv[])
{
    int server_fd, new_socket, valread;  // Descritores de socket e variável para leitura de dados
    struct sockaddr_in address;  // Estrutura para armazenar informações do endereço do servidor
    int opt = 1;  // Variável para configuração de opções do socket
    int addrlen = sizeof(address);  // Tamanho da estrutura de endereço
    char buffer[1024] = { 0 };  // Buffer para armazenar dados recebidos do cliente
    char* hello = "Hello from server";  // Mensagem de resposta a ser enviada ao cliente

    // Criação do socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Configuração para reutilizar endereço e porta
    if (setsockopt(server_fd, SOL_SOCKET,
                   SO_REUSEADDR | SO_REUSEPORT, &opt,
                   sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    // Configuração do endereço e porta do servidor
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Associação do socket com o endereço e porta
    if (bind(server_fd, (struct sockaddr*)&address,
             sizeof(address)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    // Colocando o socket em modo de escuta
    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    // Aceitando conexão de um cliente
    if ((new_socket = accept(server_fd, (struct sockaddr*)&address,
                             (socklen_t*)&addrlen)) < 0) {
        perror("accept");
        exit(EXIT_FAILURE);
    }

    // Lendo dados enviados pelo cliente
    valread = read(new_socket, buffer, 1024);
    printf("%s\n", buffer);

    // Enviando mensagem de resposta ao cliente
    send(new_socket, hello, strlen(hello), 0);
    printf("Hello message sent\n");

    // Fechando o socket da conexão
    close(new_socket);

    // Encerrando o socket do servidor
    shutdown(server_fd, SHUT_RDWR);
    return 0;
}
