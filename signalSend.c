#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <time.h>

int main(int argc, char *argv[]){

    int processId = atoi(argv[1]);
    int signal = atoi(argv[2]);

    kill(processId, signal);
    return 0;
}
