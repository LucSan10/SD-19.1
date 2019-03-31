#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>
#include <time.h>

int main(int argc, char *argv[]){

    if(argc == 1){
        printf("Missing parameters processId and signal\n");
        return 0;
    } else if(argc == 2){
        printf("Missing parameter signal\n");
        return 0;
    }

    int processId = atoi(argv[1]);
    int signal = atoi(argv[2]);

    if (0 != kill(processId, signal))
    {
        // Process doesnt exist
        printf("Process %d does not exist\n", processId);
    }

    return 0;
}
