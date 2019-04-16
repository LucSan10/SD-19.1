#include <stdio.h>
#include <stdlib.h>
#include <stdatomic.h>
#include <time.h>
#include <stdint.h>
#include <pthread.h>

int main(){
	srand(time(NULL));
	printf("%f\n", (double) rand()/RAND_MAX);
}

