#include <stdio.h>
#include <stdlib.h>
#include <stdatomic.h>
#include <time.h>
#include <stdint.h>
#include <pthread.h>
#define MIN_VALUE -100
#define MAX_VALUE 100

typedef struct{
    int start;
    int end;
} Interval;

int accumulator;
int8_t* arr;

atomic_flag lock = ATOMIC_FLAG_INIT;

void acquire(volatile atomic_flag* lock){
    while(atomic_flag_test_and_set(lock));
}

void release(volatile atomic_flag* lock){
    atomic_flag_clear(lock);
}

void populate_array_randomly(int8_t* arr, int N, int min_val, int max_val){
    for(int i = 0; i < N; i++){
        arr[i] = (int8_t) min_val + (rand() % (max_val - min_val));
    }
}

void calculate_intervals(Interval* interval, int N, int K){
    int numbers_per_thread = N/K;
    int rest = N%K;
    int i = 0;
    while(i <= N){
        interval->start = i;
        if (rest > 0){
            i++;
            rest--;
        }
        i += numbers_per_thread;
        interval->end = i;
        interval++;
    }
}

void* thread_execute_sum(void* args){
    Interval* interval = args;
    for (int i = interval->start; i < interval->end; i++){
        acquire(&lock);
        accumulator += arr[i];
        release(&lock);
    }
}

int main(int argc, char* argv[]){
    // New seed for rand().
    srand(time(NULL));

    accumulator = 0;

    if (argc < 2){
        fprintf(stderr, "Input array size missing.\n");
        exit(EXIT_FAILURE);
    }

    if (argc < 3){
        fprintf(stderr, "Input threads number missing .\n");
        exit(EXIT_FAILURE);
    }

    int N = atoi(argv[1]);
    int K = atoi(argv[2]);

    Interval* interval = (Interval*) calloc(K,sizeof(Interval));
    calculate_intervals(interval, N, K);

    arr = (int8_t*) calloc(N, 1);
    populate_array_randomly(arr, N, MIN_VALUE, MAX_VALUE);

    pthread_t thread_ids[K];

    for(int i = 0; i < K; i++){

        pthread_create(
            &thread_ids[i],
            NULL,
            thread_execute_sum,
            &interval[i]
        );
    }

    for(int i = 0; i < K; i++){
        pthread_join(thread_ids[i], NULL);
    }

    printf("\nTotal sum: %d", accumulator);
}