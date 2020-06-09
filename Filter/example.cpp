/**
 * Example Filter code
 *
 * Compiled using g++ 9.3.0
 * g++ example.cpp -o example -Wall -Werror
 *  
 * Author: redd
 */

#include <iostream>
#include "Filter.h"

int main(int argc, char** argv){

    /**
     * FIR Filter Demo
     */ 
    // load coefficients from file
    char filename[256];
    strcpy(filename, "coefficients.txt");
    std::cout << "Loading FIR filter coefficints from " << filename << std::endl;
    Filter<double> fir = Filter<double>(filename);

    // display impulse response
    std::cout << "FIR Impulse Response:" << std::endl;
    double out = fir.filter(1.0);
    while (out != 0.0){
        std::cout << "\t" << out << std::endl;
        out = fir.filter(0.0);
    }

    std::cout << "Adding a bunch of ones, displaying filter outputs:" << std::endl;
    for (int i = 0; i < 10; i++){
        std::cout << "\t" << fir.filter(1.0) << std::endl;
    }

    std::cout << "Adding a bunch of zeros, displaying filter outputs:" << std::endl;
    for (int i = 0; i < 10; i++){
        std::cout << "\t" << fir.filter(0.0) << std::endl;
    }

    std::cout << std::endl;

    /**
     * IIR Filter Demo
     */
    double b[5] = {1.0, 0.2, 0.1, 0.1, 0.1};
    double a[5] = {1.0, 0.3, 0.2, 0.1, 0.0};

    Filter<double> iir = Filter<double>(b, 5, a, 5);

    // display impulse response
    std::cout << "IIR Impulse Response:" << std::endl;
    for (int i = 0; i < 20; i++){
        std::cout << "\t" << iir.filter(1.*(i==0)) << std::endl;
    }

    return 0;
}