#define _GNU_SOURCE
#include <unistd.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdatomic.h>
#include <time.h>
#include <stdint.h>
#include <pthread.h>
#include <semaphore.h>
#include "../prime.h"

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
    sem_t* empty_buffers;
    sem_t* full_buffers;
    sem_t* mutex;
} Semaphores;

Circular_FIFO* fifo;

Semaphores* semaphores;

int* producer_count;
int* consumer_count;

int random_number_generator(int min_val, int max_val){
    int interval = max_val-min_val+1;
    double uniform = ((double) rand())/RAND_MAX;

    return min_val + (int) (uniform * interval);
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

void* producer_thread(void* args){

    int check;
    while(1){
        sem_wait(semaphores->mutex);
        (*producer_count)++;
        check = (*producer_count > ITERATION_LIMIT);
        sem_post(semaphores->mutex);

        if (check) break;

        int write = random_number_generator(MIN_VALUE, MAX_VALUE);

        sem_wait(semaphores->empty_buffers);
        sem_wait(semaphores->mutex);
        FIFO_write(write);
        sem_post(semaphores->mutex);
        sem_post(semaphores->full_buffers);
    }
}

void* consumer_thread(void* args){
    
    int check;
    while(1){
        sem_wait(semaphores->mutex);
        (*consumer_count)++;
        check = (*consumer_count > ITERATION_LIMIT);
        sem_post(semaphores->mutex);
        
        if (check) break;

        sem_wait(semaphores->full_buffers);
        sem_wait(semaphores->mutex);
        int x = FIFO_read();
        sem_post(semaphores->mutex);
        sem_post(semaphores->empty_buffers);
        
        //if (!prime(x)) printf("The number %d is not prime\n", x);
        //else printf("The number %d is prime\n", x);
    }
}

int main(int argc, char* argv[]){

    cpu_set_t producer_cpus;
    cpu_set_t consumer_cpus;

    fifo = (Circular_FIFO*) calloc(1, sizeof(Circular_FIFO));
    semaphores = (Semaphores*) calloc(1, sizeof(Semaphores));
    semaphores->mutex = (sem_t*) malloc(sizeof(sem_t));
    semaphores->empty_buffers = (sem_t*) malloc(sizeof(sem_t));
    semaphores->full_buffers = (sem_t*) malloc(sizeof(sem_t));
    producer_count = (int*) calloc(1, sizeof(int));
    consumer_count = (int*) calloc(1, sizeof(int));
    srand(time(NULL));
    
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

    sem_init(semaphores->mutex, 0, 1);
    sem_init(semaphores->empty_buffers, 0, array_size);
    sem_init(semaphores->full_buffers, 0, 0);

    if (sem_init(semaphores->mutex, 0, 1) == -1) {
        fprintf(stderr, "Semaphore mutex not inittialized.\n");
        exit(EXIT_FAILURE);
    }
    if (sem_init(semaphores->empty_buffers, 0, array_size) == -1) {
        fprintf(stderr, "Semaphore empty_buffers not inittialized.\n");
        exit(EXIT_FAILURE);
    }
    if (sem_init(semaphores->full_buffers, 0, 0) == -1) {
        fprintf(stderr, "Semaphore full_buffers not inittialized.\n");
        exit(EXIT_FAILURE);
    }

    fifo->array = (int*) calloc(array_size, sizeof(int));
    fifo->start = -1;
    fifo->end = -1;
    fifo->size = array_size;

    // measure time
    struct timespec start, finish;
    double elapsed = 0;

    for (int i = 0; i < 10; i++){

        pthread_t producer_thread_ids[producer_K];
        pthread_t consumer_thread_ids[consumer_K];

        clock_gettime(CLOCK_MONOTONIC, &start);

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

        for (int i = 0; i < producer_K; i++){
            pthread_join(producer_thread_ids[i], NULL);
        }

        for (int i = 0; i < consumer_K; i++){
            pthread_join(consumer_thread_ids[i], NULL);
        }
    
        // time-end
        clock_gettime(CLOCK_MONOTONIC, &finish);

        elapsed += (finish.tv_sec - start.tv_sec);
        elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;
    }

    elapsed /= 10;
    printf("\nN, Np, Nc = %d, %d, %d\n", array_size, producer_K, consumer_K);
    printf("Time taken to execute: %fs\n", elapsed);
    return 0;
}
