#include <stdio.h>
#include <stdlib.h>
#include <stdatomic.h>
#include <time.h>
#define MIN_VALUE -100
#define MAX_VALUE 100

atomic_flag held = ATOMIC_FLAG_INIT;

void acquire(volatile atomic_flag* lock){
    while(atomic_flag_test_and_set(lock));
}

void release(volatile atomic_flag* lock){
    atomic_flag_clear(lock);
}

int generate_random_value(int minVal, int maxVal){
    return rand() % (maxVal - minVal) + minVal;
}

void populateArrayRandomly(int* arr, int N, int minVal, int maxVal){
    for(int i = 0; i < N; i++){
        arr[i] = generate_random_value(minVal, maxVal);
    }
}

int main(int argc, char* argv[]){
    // New seed for rand().
    srand(time(NULL));

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

    int* arr = (int*) calloc(N, 1);
    populateArrayRandomly(arr, N, MIN_VALUE, MAX_VALUE);
}