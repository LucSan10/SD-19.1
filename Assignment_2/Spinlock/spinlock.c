#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdatomic.h>
#include <time.h>
#include <stdint.h>
#include <pthread.h>
#include <unistd.h>
#include <sched.h>
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
    int interval = max_val-min_val+1;
    for(int i = 0; i < N; i++){
        double uniform = ((double) rand())/RAND_MAX;
        arr[i] = (int8_t) min_val + (int8_t) (uniform * interval);
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
    int temp = 0;
    
    for (int i = interval->start; i < interval->end; i++){
        temp += (int) arr[i];
    }
    
    acquire(&lock);
    accumulator += temp;
    release(&lock);
}

int main(int argc, char* argv[]){
    // New seed for rand().
    srand(time(NULL));

    cpu_set_t cpus;

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

    // measure time
    double cpu_time_used = 0;
    clock_t start, end;

    for (int i = 0; i < 10; i++){
        accumulator = 0;
        pthread_t thread_ids[K];

        pthread_attr_t attr;
        pthread_attr_init(&attr);
        
        start = clock();

        for(int i = 0; i < K; i++){

            CPU_ZERO(&cpus);
            CPU_SET(i%4, &cpus);
            pthread_attr_setaffinity_np(&attr, sizeof(cpu_set_t), &cpus);

            pthread_create(
                &thread_ids[i],
                &attr,
                thread_execute_sum,
                &interval[i]
            );
        }

        for(int i = 0; i < K; i++){
            pthread_join(thread_ids[i], NULL);
        }
        
        // time-end
        end = clock();
        cpu_time_used += ((double) (end - start)) / CLOCKS_PER_SEC;

        
        // printf("[");
        // for (int i = 0; i < N-1; i++){
        //     printf("%d, ", arr[i]);
        // }
        // printf("%d]", arr[N-1]);

        printf("Total sum: %d\n", accumulator);
    }
    printf("\nK, N = %d, %d\n", K, N);
    cpu_time_used /= 10;
    
    printf("Time taken to execute: %f s\n", cpu_time_used);
}