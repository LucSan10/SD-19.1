#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <time.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define MSGSIZE 20
#define PORT 8088

int server_socket(){
    int server_fd, new_socket;
    struct sockaddr_in server_addr, client_addr;
    char buffer[MSGSIZE] = {0};

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0){
        fprintf(stderr, "Socket Failed.");
        exit(EXIT_FAILURE);
    }

    int server_chain = bind(server_fd, (struct sockaddr*) &server_addr, sizeof(server_addr));
    if (server_chain < 0){
        fprintf(stderr, "Bind Failed.");
        exit(EXIT_FAILURE);
    }

    int server_ears = listen(server_fd, 5);
    if (server_ears < 0){
        fprintf(stderr, "Listen Failed.");
        exit(EXIT_FAILURE);
    }

    new_socket = accept(server_fd, (struct sockaddr*) &client_addr, sizeof(client_addr));
    if (new_socket < 0){
        fprintf(stderr, "Accept Failed.");
        exit(EXIT_FAILURE);
    }
}