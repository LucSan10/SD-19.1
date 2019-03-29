#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <time.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <netdb.h>

#define MSGSIZE 20
#define PORT 4567

int main(int argc, char* argv[]){
    struct sockaddr_in client_addr, server_addr;
    int client_fd;
    char read_n[MSGSIZE], write_n[MSGSIZE];
    
    int number = 1;

    if (argc < 2){
        fprintf(stderr, "Input number not specified.\n");
        exit(EXIT_FAILURE);
    }

    client_fd = socket(AF_INET, SOCK_STREAM, 0);
    
    if (client_fd < 0){
        fprintf(stderr, "\nClient Socket Failed.\n");
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, '0', sizeof(server_addr));
    server_addr.sin_family = AF_INET; 
    server_addr.sin_port = htons(PORT);

    if(inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr) < 0){ 
        printf("\nInvalid address/Address not supported\n"); 
        exit(EXIT_FAILURE);
    }

    if (connect(client_fd, (struct sockaddr*) &server_addr, sizeof(server_addr)) < 0) 
    { 
        fprintf(stderr, "\nClient Connection Failed\n"); 
        exit(EXIT_FAILURE);
    }

    srand(time(NULL));
    int how_many = atoi(argv[1]);

    for (int i = 0; i < how_many; i++){
        number += rand() % 100;
        sprintf(write_n, "%d", number);
        send(client_fd, write_n, MSGSIZE, 0);

        read(client_fd, read_n, MSGSIZE);

        if (atoi(read_n)) printf("Yes.\n");
        else printf("No.\n");
    }

    send(client_fd, "0", MSGSIZE, 0);

    // Erase client socket
    shutdown(client_fd, 2);
    printf("\nCLIENT SIGTERM\n");

    exit(0);
}