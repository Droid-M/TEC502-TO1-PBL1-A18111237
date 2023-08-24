#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include "cJSON.h" // Inclua o cabeçalho da biblioteca cJSON

#define PORT 8080

int main(int argc, char const *argv[])
{
    int server_fd, new_socket, valread;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);
    char buffer[1024] = {0};
    char *hello = "Hello from server";
    cJSON *received_json = NULL; // Objeto JSON para armazenar o JSON recebido

    // Criação do socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Restante do código de configuração do servidor

    while (1)
    {
        // Aceitar conexão e receber dados JSON
        iif((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0)
        {
            if (errno == EWOULDBLOCK || errno == EAGAIN)
            {
                // Timeout, faça alguma ação ou apenas continue o loop
                continue;
            }
            else
            {
                perror("accept");
                exit(EXIT_FAILURE);
            }
        }
        valread = read(new_socket, buffer, 1024);

        // Analisar o JSON recebido
        received_json = cJSON_Parse(buffer);
        if (received_json)
        {
            cJSON *message = cJSON_GetObjectItem(received_json, "message");
            cJSON *value = cJSON_GetObjectItem(received_json, "value");

            if (message && value)
            {
                printf("Received message: %s\n", message->valuestring);
                printf("Received value: %d\n", value->valueint);
            }
            else
            {
                printf("Received JSON is missing required fields.\n");
            }

            // Enviar resposta JSON
            cJSON *response_json = cJSON_CreateObject();
            cJSON_AddStringToObject(response_json, "response", "Data received successfully");
            char *response_string = cJSON_Print(response_json);
            send(new_socket, response_string, strlen(response_string), 0);

            // Limpar memória
            cJSON_Delete(received_json);
            cJSON_Delete(response_json);
            free(response_string);
        }
        else
        {
            printf("Invalid JSON received.\n");
        }

        // Fechar o socket do cliente
        close(new_socket);
    }

    // Fechamento do socket do servidor
    shutdown(server_fd, SHUT_RDWR);
    return 0;
}