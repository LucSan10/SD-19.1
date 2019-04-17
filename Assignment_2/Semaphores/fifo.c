#include <stdio.h>
#include <stdlib.h>
#include <stdatomic.h>
#include <time.h>
#include <stdint.h>
#include <pthread.h>
#include "../prime.h"

typedef struct{
    int* array;
    int size;
    int start;
    int end;
} Circular_FIFO;

Circular_FIFO* fifo;

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