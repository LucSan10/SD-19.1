#!/bin/bash

N=$((10**1))
for i in {1..3}
do
    M=$((1))
    for j in {1..3}
    do
        ./spinlock $N $M
        M=$((M*2))
    done
    N=$((N*10))
done