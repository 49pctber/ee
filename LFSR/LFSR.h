/**
 * Linear Feedback Shift Register for generating pseudorandom bit sequences.
 * 
 * Specify length of LFSR, taps, or use default settings.
 * 
 * Author: redd
 */ 

#ifndef LFSR_H
#define LFSR_H

#include <math.h>
#include <cmath>
#include <stdio.h>
#include <bitset>

class LFSR{
    public:
        LFSR(); // initialize with 32-bit lfsr
        LFSR(unsigned int l); // initialize with maximum-length l-bit lfsr (limited # of lengths supported)
        LFSR(unsigned int l, unsigned int taps); // manually set taps by specifying bitmask
        void setSeed(unsigned int); // sets registers of lfsr for repeatability

        unsigned int getNextBit(); // gets the next pseudorandom bit
        unsigned int getNext(); // gets the next value stored by registers
        unsigned int getBitmask(); // returns the bitmask used by lfsr

    private:
        void init(unsigned int l, unsigned int taps);
        unsigned int bitmask;
        unsigned int taps;
        unsigned int r;
        unsigned int l;
};

#endif