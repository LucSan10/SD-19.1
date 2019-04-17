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
#define MAX_VALUE 100
#define ITERATION_LIMIT 1000

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

static Circular_FIFO* fifo;

static Semaphores* semaphores;

static int* iteration_limit;

int random_number_generator(int min_val, int max_val){
    int interval = max_val-min_val+1;
    double uniform = ((double) rand())/RAND_MAX;

    return min_val + (int) (uniform * interval);
}

void wait(int* semaphore){
    while (*semaphore <= 0);
    (*semaphore)--;
}

void signal(int* semaphore){
    (*semaphore)++;
}

void* producer_thread(void* args){
    while(*iteration_limit > 0){
        int write = random_number_generator(MIN_VALUE, MAX_VALUE);

        wait(&semaphores->not_full);
        wait(&semaphores->mutex);
        FIFO_write(write);
        signal(&semaphores->mutex);
        signal(&semaphores->not_empty);
        
        printf("Next value: %d\n", write);
    }
}

void* consumer_thread(void* args){
    while(*iteration_limit > 0){
        wait(&semaphores->not_empty);
        wait(&semaphores->mutex);
        int x = FIFO_read();
        signal(&semaphores->mutex);
        signal(&semaphores->not_full);
        
        (*iteration_limit)--;
        
        if (!prime(x)) printf("The number %d is not prime\n", x);
        else printf("The number %d is prime\n", x);
    }
}

int FIFO_read(){
    fifo->start = (fifo->start + 1) % fifo->size;
    int number_to_read = fifo->array[fifo->start];
    fifo->array[fifo->start] = 0;
    return number_to_read;
}

void FIFO_write(int number_to_write){
    fifo->end = (fifo->end + 1) % fifo->size;
    fifo->array[fifo->end] = number_to_write;
}

int main(int argc, char* argv[]){
    fifo = (Circular_FIFO*) calloc(1, sizeof(Circular_FIFO));
    semaphores = (Semaphores*) calloc(1, sizeof(Semaphores));
    iteration_limit = (int*) malloc(sizeof(int));

    srand(time(NULL));

    semaphores->not_empty = 0;
    semaphores->mutex = 1;

    if (argc < 2){
        fprintf(stderr, "Array size missing.\n");
        exit(EXIT_FAILURE);
    }

    if (argc < 3){
        fprintf(stderr, "Number of producer threads missing.\n");
        exit(EXIT_FAILURE);
    }

    if (argc < 4){
        fprintf(stderr, "Number of consumer threads missing.\n");
        exit(EXIT_FAILURE);
    }

    int array_size = atoi(argv[1]);
    int producer_K = atoi(argv[2]);
    int consumer_K = atoi(argv[3]);
    *iteration_limit = ITERATION_LIMIT;

    semaphores->not_full = array_size;

    fifo->array = (int*) calloc(array_size, sizeof(int));
    fifo->start = -1;
    fifo->end = -1;
    fifo->size = array_size;

    // measure time
    clock_t start, end;
    double cpu_time_used;
    start = clock();

    pthread_t producer_thread_ids[producer_K];
    pthread_t consumer_thread_ids[consumer_K];

    for (int i = 0; i < producer_K; i++){
        pthread_create(
            &producer_thread_ids[i],
            NULL,
            producer_thread,
            NULL
        );
    }

    for (int i = 0; i < consumer_K; i++){
        pthread_create(
            &consumer_thread_ids[i],
            NULL,
            consumer_thread,
            NULL
        );
    }

    // for (int i = 0; i < consumer_K; i++){
    //     pthread_join(consumer_thread_ids[i], NULL);
    // }

    printf("Consumer threads joined.\n");

    // for (int i = 0; i < producer_K; i++){
    //     pthread_join(producer_thread_ids[i], NULL);
    // }

    printf("Producer threads joined.\n");

    // time-end
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("Time taken to execute: %f s\n", cpu_time_used);
    return 0;
}