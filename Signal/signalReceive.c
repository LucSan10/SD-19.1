#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <time.h>

// SIGINT = 2
void myHandlerInt (int param)
{
    printf("handler Int \n");
}

// SIGILL = 4
void myHandlerIll (int param)
{
    printf("handler Ill \n");
}

// SIGTERM = 15
void myHandlerTerm (int param)
{
    printf("handler Term \n");
    exit(0);
}

void startBusyWait(){
    printf("starting busy wait \n");
    while (1){
        pause();
    }
}

int main(int argc, char *argv[]){
    printf("Process id: %d\n", ::getpid());

    void (*intHandler)(int);
    void (*illHandler)(int);
    void (*termHandler)(int);

    intHandler = signal (SIGINT, myHandlerInt);
    illHandler = signal (SIGILL, myHandlerIll);
    termHandler = signal (SIGTERM, myHandlerTerm);

    if(argc < 2){
        printf("Missing parameter for type of wait \n");
        return 0;
    } else if (atoi(argv[1])==0){
        startBusyWait();
    } else {
        
    }

    return 0;
}
