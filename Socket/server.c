#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include "../prime.h"

#define MSGSIZE 20
#define PORT 4567


int main(int argc, char* argv[]){
    int opt = 1;
    int client_fd, server_fd;
    socklen_t cli_addr;
    char read_n[MSGSIZE], write_n[MSGSIZE];
    struct sockaddr_in server_addr, client_addr;

    // Server socket accepts only IPv4 adresses
    server_addr.sin_family = AF_INET;

    // Server socket assigns its address to localhost
    server_addr.sin_addr.s_addr = INADDR_ANY;

    // Server port trasnformed to network byte order
    server_addr.sin_port = htons(PORT);

    // Creation socket
    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0){
        fprintf(stderr, "\nServer Socket Failed.\n");
        exit(EXIT_FAILURE);
    }

    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        fprintf(stderr, "\nOperation Failed.\n");
        exit(EXIT_FAILURE);
    }

    // Binding address to socket
    int server_chain = bind(server_fd, (struct sockaddr*) &server_addr, sizeof(server_addr));
    if (server_chain < 0){
        fprintf(stderr, "\nBind Failed.\n");
        exit(EXIT_FAILURE);
    }

    // Make socket listen
    int server_ears = listen(server_fd, 5);
    if (server_ears < 0){
        fprintf(stderr, "\nListen Failed.\n");
        exit(EXIT_FAILURE);
    }

    cli_addr = sizeof(client_addr);
    client_fd = accept(server_fd, (struct sockaddr*) &client_addr, &cli_addr);
    if (client_fd < 0){
        fprintf(stderr, "\nAccept Failed.\n");
        exit(EXIT_FAILURE);
    }

    
    read(client_fd, read_n, MSGSIZE);
    int out = atoi(read_n);

    // Until the server receives a 0, do:
    while (out){
        printf("\nIs number %d prime?\n", out);

        // Send result of the current number's primality check to the client.
        if (prime(out)) send(client_fd, "1", MSGSIZE, 0);
        else send(client_fd, "0", MSGSIZE, 0);

        // Read the next number
        read(client_fd, read_n, MSGSIZE);
        out = atoi(read_n);
    }

    // Erase the server socket
    shutdown(server_fd, 2);
    printf("\nSERVER SIGTERM\n");

    exit(0);
}