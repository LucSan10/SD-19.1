#include <stdio.h>
#include <stdlib.h>
#include <stdatomic.h>


atomic_flag held = ATOMIC_FLAG_INIT;

void acquire(volatile atomic_flag* lock){
    while(atomic_flag_test_and_set(lock));
}

void release(volatile atomic_flag* lock){
    atomic_flag_clear(lock);
}

int main(){
    
}