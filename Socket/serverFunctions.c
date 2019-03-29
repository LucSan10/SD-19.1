#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <time.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include "../prime.h"

#define MSGSIZE 20
#define PORT 8088


void server_socket_create(){
    int server_fd, client_fd;
    int opt = 1;
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
        fprintf(stderr, "Socket Failed.");
        exit(EXIT_FAILURE);
    }

    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        fprintf(stderr, "Operation Failed.");
        exit(EXIT_FAILURE);
    }

    // Binding address to socket
    int server_chain = bind(server_fd, (struct sockaddr*) &server_addr, sizeof(server_addr));
    if (server_chain < 0){
        fprintf(stderr, "Bind Failed.");
        exit(EXIT_FAILURE);
    }

    // Make socket listen
    int server_ears = listen(server_fd, 5);
    if (server_ears < 0){
        fprintf(stderr, "Listen Failed.");
        exit(EXIT_FAILURE);
    }

    client_fd = accept(server_fd, (struct sockaddr*) &client_addr, sizeof(client_addr));
    if (client_fd < 0){
        fprintf(stderr, "Accept Failed.");
        exit(EXIT_FAILURE);
    }
}

int server_socket_rw(int client_fd, int server_fd){
    
    char read_n[MSGSIZE];
    read(client_fd, read_n, MSGSIZE);
    int out = atoi(read_n);

    while (out){
        printf("Is number %d prime?\n", out);

        if (prime(out)) send(client_fd, "Yes.", MSGSIZE, 0);
        else send(client_fd, "No.", MSGSIZE, 0);

        read(client_fd, read_n, MSGSIZE);
        out = atoi(read_n);
    }

    shutdown(server_fd, 2);
    return 0;
}