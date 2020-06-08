#include "LFSR.h"

LFSR::LFSR(){
    this->init(32, 0b10100011000000000000000000000000);
}

LFSR::LFSR(unsigned int l){
    switch(l){
        case 32:
            this->init(32, 0b10100011000000000000000000000000);
            break;
        case 31:
            this->init(31, 0b1001000000000000000000000000000);
            break;
        case 24:
            this->init(24, 0b1101100000000000000000000);
            break;
        case 20:
            this->init(20, 0b11001010000000000000);
            break;
        case 16:
            this->init(16, 0b101101000000000);
            break;
        case 12:
            this->init(12, 0b110010100000);
            break;
        case 11:
            this->init(11, 0b11101000000);
            break;
        case 10:
            this->init(10, 0b1101100000);
            break;
        case 9:
            this->init(9, 0b110110000);
            break;
        case 8:
            this->init(8, 0b10111000);
            break;
        case 7:
            this->init(7, 0b1111000);
            break;
        case 6:
            this->init(6, 0b110110);
            break;
        case 5:
            this->init(5, 0b11110);
            break;
        case 4:
            this->init(4, 0b1100);
            break;
        case 3:
            this->init(3, 0b110);
            break;
        case 2:
            this->init(2, 0b11);
            break;
    }
}

LFSR::LFSR(unsigned int l, unsigned int taps){
    this->init(l, taps);
}

void LFSR::init(unsigned int l, unsigned int taps){
    r = 0b1;
    this->l = l;
    this->bitmask = 0b0;
    for (unsigned int i = 0; i < l; i++){
        this->bitmask = (this->bitmask << 1) | 0b1;
    }
    this->taps = taps & this->bitmask;
    this->setSeed(0xDEADBEEF);
}

void LFSR::setSeed(unsigned int seed){
    this->r = seed;
}

unsigned int LFSR::getNextBit(){
    return 0b1 & this->getNext();
}

unsigned int LFSR::getNext(){
    unsigned int n = this->taps & this->r;
    unsigned int c = 0b0;

    for (unsigned int i = 0; i < l; i++){
        c += n & 0b1;
        n = n >> 1;
    }

    this->r = (this->r << 1) & this->bitmask;
    this->r = this->r ^ (0b1 & c);

    return this->r;
}

unsigned int LFSR::getBitmask(){
    return this->bitmask;
}
