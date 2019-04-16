#include <stdio.h>
#include <stdlib.h>
#include <stdatomic.h>
#include <time.h>
#include <stdint.h>
#include <pthread.h>
#define MIN_VALUE 1
#define MAX_VALUE 10000000

typedef struct{
    int* array;
    int end;
    int start;
    int size;
} Circular_FIFO;

Circular_FIFO fifo;

int FIFO_read(Circular_FIFO* fifo, int* number_to_read){
    if (fifo->start == fifo->end) return -1;
    fifo->start = (fifo->start + 1) % fifo->size;
    *number_to_read = fifo->array[fifo->start];
    return 0;
}

int FIFO_write(Circular_FIFO* fifo, int number_to_write){
    if ()   
}

void* consumer_thread(void* args){

}

void* producer_thread(void* args){

}

int random_number_generator(int min_val, int max_val){
    int interval = max_val-min_val+1;
    double uniform = ((double) rand())/RAND_MAX;

    return min_val + (int) (uniform * interval);
}

int main(int argc, char* argv[]){

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

    int array_size = atoi(argv[1]) + 1;
    int producer_N = atoi(argv[2]);
    int consumer_N = atoi(argv[3]);

    fifo.array = (int*) calloc(array_size, sizeof(int));
    fifo.start = 0;
    fifo.end = 0;
    fifo.size = array_size;
}