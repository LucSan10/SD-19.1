#include <stdio.h>
#include <stdlib.h>

int prime(int n){

    // All positive integers lower than or equal to 3 are primes
    if (n <= 3) return 1;
    // ...except for 1. Also, numbers divisible by 2 or 3 are obviously not prime.
    if (n == 1 || !(n%2 && n%3)) return 0;
    
    // For any integer x:
    // (6x+0), (6x+2) and (6x+4) are divisible by, and (6x+3) is divisible by 3, so
    // (6x+1) and (6x+5 == 6(x+1)-1 --> 6x-1) are possibly primes

    for (int i = 5; i*i<=n; i+=6){

        // If a number is prime, then it is not divisible
        // by any other primes (6x+1 or 6x-1) other than itself.
        if (!(n%i && n%(i+2))) return 0;
    }

    return 1;
}