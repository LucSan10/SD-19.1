#include <stdio.h>
#include <stdlib.h>
#include <stdatomic.h>
#include <time.h>
#include <stdint.h>
#include <pthread.h>
#include "../prime.h"

typedef struct{
    int not_full;
    int not_empty;
    int mutex;
} Semaphores;

void wait(int* semaphore){
    while (*semaphore <= 0);
    (*semaphore)--;
}

void signal(int* semaphore){
    (*semaphore)++;
}