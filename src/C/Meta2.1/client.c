// Client side C/C++ program to demonstrate Socket
// programming
#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include "cJSON.h"  // Inclua o cabeçalho da biblioteca cJSON

#define PORT 8080

int main(int argc, char const* argv[])
{
    int status, valread, client_fd;
    struct sockaddr_in serv_addr;
    cJSON* json = NULL;  // Objeto JSON para construir a mensagem
    char* json_string = NULL;  // String para armazenar o JSON serializado
    char buffer[1024] = { 0 };

    // Criação do socket do cliente
    if ((client_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("\n Socket creation error \n");
        return -1;
    }

    // Configuração do endereço e porta do servidor
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

    // Conversão do endereço IP de texto para binário
    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) <= 0) {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }

    // Conexão ao servidor
    if ((status = connect(client_fd, (struct sockaddr*)&serv_addr, sizeof(serv_addr))) < 0) {
        printf("\nConnection Failed \n");
        return -1;
    }

    // Criar um objeto JSON e preenchê-lo com dados
    json = cJSON_CreateObject();
    cJSON_AddStringToObject(json, "message", "Hello from client");
    cJSON_AddNumberToObject(json, "value", 42);

    // Converter o objeto JSON para string
    json_string = cJSON_Print(json);

    // Enviar o JSON como string para o servidor
    send(client_fd, json_string, strlen(json_string), 0);

    // Limpar memória do objeto JSON
    cJSON_Delete(json);
    free(json_string);

    // Leitura da resposta do servidor
    valread = read(client_fd, buffer, 1024);
    printf("Server response: %s\n", buffer);

    // Fechamento do socket conectado
    close(client_fd);

    return 0;
}