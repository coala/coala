// Include a whole lot of stuff - shouldn't influence the counting!
#include <stdio.h>
#include "not_existant.c"

// Empty function
int test(void);

// Global variable, shouldn't be counted
int g;

// A function with a few parameters
int main(int t, char* args) {
    // Usage in a call
    smile(t, g);

    // Simple stupid assignment
    t = g;

    // Local declaration
    int *asd;

    // Simple more stupid reassignment, this time using other syntax elems
    t = args[g];

    // Declaration in for loop
    for(int i; i < 5; i++) {
        // Checking out constants
        printf("i is %d", i);
    }
}
