#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <time.h>
#include "pipeFunctions.h"
#include "../prime.h"

// Size of each message.
#define MSGSIZE 20

int pipe_creator(int how_many){

    // Array for pipe read/write.
    int fd[2];
    
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
        father(fd, how_many);
        exit(EXIT_SUCCESS);
    }

    // Child process: fork == 0
    else{
        child(fd);
        exit(EXIT_SUCCESS);
    }
    return 0;
}

int main(int argc, char* argv[]){

    if (argc < 2){
        fprintf(stderr, "Input number not specified.\n");
        exit(EXIT_FAILURE);
    }

    if (argv[1] < 0){
        fprintf(stderr, "Input number cannot be negative.\n");
        exit(EXIT_FAILURE);
    }

    int n = atoi(argv[1]);

    pipe_creator(n);
    return 0;
}
