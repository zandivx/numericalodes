#ifndef MATRIX_H
#define MATRIX_H
#include <stddef.h>

typedef struct matrix
{
    double **pptr; // address of array
    size_t r;      // number of rows
    size_t c;      // number of columns
} matrix;

void create_m(matrix m);
void delete_m(matrix m);
double get_e(matrix m, size_t i, size_t j);           // get element
double *get_r(matrix m, size_t i);                    // get row
void set(matrix m, size_t i, size_t j, double value); // set element
void transpose(matrix m);
void print_m(matrix m);
void fprint_m(matrix m, char *path);

#endif