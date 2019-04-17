#include <stdio.h>
#include <stdlib.h>
#include <stdatomic.h>
#include <time.h>
#include <stdint.h>
#include <pthread.h>
#include "../prime.h"
#include "fifo.h"
#include "semaphoreFunctions.h"
#define MIN_VALUE 1
#define MAX_VALUE 10000000
#define ITERATION_LIMIT 100000

typedef struct{
    int* array;
    int size;
    int start;
    int end;
} Circular_FIFO;

typedef struct{
    int not_full;
    int not_empty;
    int mutex;
} Semaphores;

Circular_FIFO* fifo;

Semaphores* semaphores;

int* iteration_limit;

int random_number_generator(int min_val, int max_val){
    int interval = max_val-min_val+1;
    double uniform = ((double) rand())/RAND_MAX;

    return min_val + (int) (uniform * interval);
}

void* producer_thread(void* args){
    while(*iteration_limit > 0){
        int write = 1;

        wait(&(semaphores->not_full));
        wait(&(semaphores->mutex));
        FIFO_write(write);
        signal(&(semaphores->mutex));
        signal(&(semaphores->not_empty));
        
        printf("Next value: %d", write);
    }
}

void* consumer_thread(void* args){
    while(*iteration_limit > 0){
        wait(&(semaphores->not_empty));
        wait(&(semaphores->mutex));
        int x = FIFO_read();
        signal(&(semaphores->mutex));
        signal(&(semaphores->not_full));
        
        (*iteration_limit)--;
        
        printf("The number %d is ", x);
        if (!prime(x)) printf("not ");
        printf("prime.\n");
    }
}

int main(int argc, char* argv[]){
    srand(time(NULL));

    printf("uhhh");

    semaphores = (Semaphores*) calloc(1, sizeof(Semaphores));

    semaphores->not_empty = 0;
    semaphores->mutex = 1;

    // printf("hey\n");
}