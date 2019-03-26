#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <time.h>
#include "pipeFunctions.h"

// Size of each message.
#define MSGSIZE 20

int pipeC(int how_many){

    // Array for pipe read/write.
    int fd[2];
    
    // Starting number.
    int number = 1;
    
    // New seed for rand().
    srand(time(NULL));

    // Returns 0 if created, -1 if not.
    int p = pipe(fd);
    
    if (p < 0){
        fprintf(stderr, "Pipe Failed.");
        exit(EXIT_FAILURE);
    }

    // Returns 0+ if created, -1 if not.
    int f = fork();
    if (f < 0){
        fprintf(stderr, "Fork Failed.");
        exit(EXIT_FAILURE);
    }

    // Father process: fork > 0
    else if (f > 0){
        // Impede-se a leitura.
        close(fd[0]);
        char write_n[MSGSIZE];
        
        for (int i = 0; i < how_many; i++){
            number += rand() % 100;
            sprintf(write_n, "%d", number);
            write(fd[1], write_n, MSGSIZE);
        }

        write(fd[1], "0", MSGSIZE);
        close(fd[1]);
        exit(EXIT_SUCCESS);
    }

    // Child process: fork == 0
    else{
        // Impede-se a escrita.
        close(fd[1]);
        
        char read_n[MSGSIZE];
        read(fd[0], read_n, MSGSIZE);
        int out = atoi(read_n);

        while (out){
            printf("Is number %d prime?\n", out);

            if (prime(out)) printf("Yes.\n\n");
            else printf("No.\n\n");

            read(fd[0], read_n, MSGSIZE);
            out = atoi(read_n);
        }

        printf("SIGTERM\n\n");
        close(fd[0]);
        exit(EXIT_SUCCESS);
    }
    return 0;
}

int main(int argc, char* argv[]){
    
    if (argc < 2){
        fprintf(stderr, "Input number not specified.\n");
        exit(EXIT_FAILURE);
    }

    int n = atoi(argv[1]);

    pipeC(n);
    return 0;
}