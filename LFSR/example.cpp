/**
 * Example code using LFSR.h
 * 
 * Uses the current time to set the seed of the LFSR then displays a pseudorandom bit sequence.
 * 
 * compiled and ran using g++ 9.3.0 on Ubuntu using command
 * g++ *.cpp -o example -Wall -Werror
 * ./example
 * 
 * Author: redd
 */ 

#include <iostream>
#include <ctime>
#include "LFSR.h"

#define NBITS (1024)

int main(int argc, char** argv){
    
    // initialize 32-bit mamimal-length LFSR
    LFSR lfsr = LFSR();

    // set the seed of the LFSR based on the current time
    time_t now = time(0);
    localtime(&now);
    now = now ^ (now << 8) ^ (now << 16) ^ (now << 24);
    lfsr.setSeed(now);

    // display NBITS pseudorandom bits
    std::cout << "Generating pseudorandom bit sequence:" << std::endl;
    for (int i = 0; i < NBITS; i++){
        std::cout << lfsr.getNextBit();
    }
    std::cout << std::endl;
    
    return 0;
}