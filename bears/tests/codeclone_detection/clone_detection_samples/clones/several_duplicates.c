/* This file is merely to test the statistics output of the clang clone
   detection bear. */

int main(int a) {
    a = a + 1;
    return a + 1;
}

int something(int b) {
    b = b + 1;
    return b + 1
}

int other(int b) {
    b = b + 1;
    return b + 1
}
