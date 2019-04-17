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

static Circular_FIFO* fifo;

static Semaphores* semaphores;

static int* iteration_limit;

int random_number_generator(int min_val, int max_val){
    int interval = max_val-min_val+1;
    double uniform = ((double) rand())/RAND_MAX;

    return min_val + (int) (uniform * interval);
}

void* producer_thread(void* args){
    while(*iteration_limit > 0){
        int write = random_number_generator(MIN_VALUE, MAX_VALUE);

        wait(&semaphores->not_full);
        wait(&semaphores->mutex);
        FIFO_write(write);
        signal(&semaphores->mutex);
        signal(&semaphores->not_empty);
        
        printf("Next value: %d", write);
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
        
        printf("The number %d is ", x);
        if (!prime(x)) printf("not ");
        printf("prime.\n");
    }
}

int main(int argc, char* argv[]){
    fifo = (Circular_FIFO*) calloc(1, sizeof(Circular_FIFO));
    semaphores = (Semaphores*) calloc(1, sizeof(Semaphores));
    iteration_limit = (int*) malloc(sizeof(int));

    srand(time(NULL));

    semaphores->not_empty = 0;
    semaphores->mutex = 1;

    printf("hey\n");

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

    printf("heyy\n");

    int array_size = atoi(argv[1]);
    int producer_K = atoi(argv[2]);
    int consumer_K = atoi(argv[3]);
    *iteration_limit = ITERATION_LIMIT;

    semaphores->not_full = array_size;

    fifo->array = (int*) calloc(array_size, sizeof(int));
    fifo->start = -1;
    fifo->end = -1;
    fifo->size = array_size;

    printf("heyyy\n");

    // measure time
    clock_t start, end;
    double cpu_time_used;
    start = clock();

    pthread_t producer_thread_ids[producer_K];
    pthread_t consumer_thread_ids[consumer_K];

    printf("Starting\n");

    for (int i = 0; i < producer_K; i++){
        pthread_create(
            &producer_thread_ids[i],
            NULL,
            producer_thread,
            NULL
        );
    }

    printf("Producer threads created.\n");

    for (int i = 0; i < consumer_K; i++){
        pthread_create(
            &consumer_thread_ids[i],
            NULL,
            consumer_thread,
            NULL
        );
    }

    printf("Consumer threads created.\n");

    for (int i = 0; i < producer_K; i++){
        pthread_join(producer_thread_ids[i], NULL);
    }

    for (int i = 0; i < consumer_K; i++){
        pthread_join(consumer_thread_ids[i], NULL);
    }

    // time-end
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
}