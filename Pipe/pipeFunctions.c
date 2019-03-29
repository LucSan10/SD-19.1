#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <time.h>
#include "../prime.h"
#include "pipeFunctions.h"

// Size of each message.
#define MSGSIZE 20

void father(int fd[2], int how_many){
    
    int number = 1;
    close(fd[0]);
    char write_n[MSGSIZE];
    
    for (int i = 0; i < how_many; i++){
        number += rand() % 100;
        sprintf(write_n, "%d", number);
        write(fd[1], write_n, MSGSIZE);
    }

    write(fd[1], "0", MSGSIZE);
    close(fd[1]);
}

void child(int fd[2]){
    
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
}