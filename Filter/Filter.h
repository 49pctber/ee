/**
 * A basic filter class for FIR and IIR filters.
 * 
 * Implements transfer function
 * (b0 + b1*z^-1 + b2*z^-2 + ...) / (a0 + a1*z^-1 + a2*z^-2 + ...)
 * 
 * You can load FIR filter coefficients from a file.
 * Coefficients must be on separate rows, with b0 on the first row, b1 on the second, etc.
 * 
 * Author: redd
 */

#ifndef FILTER_H
#define FILTER_H

#include <deque>
#include <cstring>
#include <fstream>

template <typename data_t>
class Filter{
    public:
        Filter(char* filename); // FIR from file
        Filter(data_t* b_coeffs, const unsigned int b_len); // FIR
        Filter(data_t* b_coeffs, const unsigned int b_len, data_t* a_coeffs, const unsigned int a_len); // IIR
        ~Filter();
        data_t filter(data_t input);

    private:
        data_t* a; // denominator coefficients
        data_t* b; // numerator coefficients
        unsigned int a_len;
        unsigned int b_len;
        std::deque<data_t> input_d; // delayed inputs
        std::deque<data_t> output_d; // delayed outputs
        void init_coeffs(data_t* b_coeffs, const unsigned int b_len, data_t* a_coeffs, const unsigned int a_len);
};

template <typename data_t>
void Filter<data_t>::init_coeffs(data_t* b_coeffs, const unsigned int b_len, data_t* a_coeffs, const unsigned int a_len){
    
    this->a_len = a_len;
    this->b_len = b_len;

    this->a = new data_t[a_len];
    this->b = new data_t[b_len];

    for (unsigned int i = 0; i < a_len; i++){
        this->a[i] = a_coeffs[i] / a_coeffs[0];
        this->output_d.push_front(0);
    }

    for (unsigned int i = 0; i < b_len; i++){
        this->b[i] = b_coeffs[i] / a_coeffs[0];
        this->input_d.push_front(0);
    }

}


template <typename data_t>
Filter<data_t>::Filter(data_t* b_coeffs, const unsigned int b_len){
    const unsigned int a_len = 1;
    data_t a_coeffs[a_len] = {1.0};
    this->init_coeffs(b_coeffs, b_len, a_coeffs, a_len);
}

template <typename data_t>
Filter<data_t>::Filter(data_t* b_coeffs, const unsigned int b_len, data_t* a_coeffs, const unsigned int a_len){
    this->init_coeffs(b_coeffs, b_len, a_coeffs, a_len);
}

template <typename data_t>
Filter<data_t>::Filter(char* filename){
    
    std::fstream file;
    file.open(filename, std::ios::in);
    
    std::deque<data_t> vals;
    data_t val;

    while (!file.eof()){
        file >> val;
        vals.push_back(val);
    }
    vals.pop_back(); // get rid of garbage value b/c newline character
    file.close();

    const unsigned int b_len = vals.size();

    const unsigned int a_len = 1;
    data_t a_coeffs[a_len] = {1.0};

    data_t b_coeffs[b_len];

    for (unsigned int i = 0; i < b_len; i++){
        b_coeffs[i] = vals[i];
    }

    this->init_coeffs(b_coeffs, b_len, a_coeffs, a_len);

}

template <typename data_t>
Filter<data_t>::~Filter(){
    delete[] this->a;
    delete[] this->b;
}

template <typename data_t>
data_t Filter<data_t>::filter(data_t input){

    this->input_d.push_front(input);

    // generate output
    data_t val = 0.0;
    for (unsigned int i = 0; i < this->b_len; i++){
        val += this->b[i] * this->input_d[i];
    }
    for (unsigned int i = 1; i < this->a_len; i++){
        val -= this->a[i] * this->output_d[i-1];
    }

    // update delayed values
    this->output_d.push_front(val);
    this->input_d.pop_back();
    this->output_d.pop_back();

    return this->output_d[0];
}



#endif 