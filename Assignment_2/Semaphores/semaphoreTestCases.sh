#!/bin/bash

./semaphore 1 1 1

N=$((1))
for i in {1..6}
do
    M=$((2))
    for j in {1..4}
    do
        ./semaphore $N 1 $M
        ./semaphore $N $M 1
        M=$((M*2))
    done
    N=$((N*2))
done