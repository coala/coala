int used(int a, int b) {
    for(a=0; a < b; b++) {
        a += b;
    }

    while(a) {
        foo(b);
    }

    return b;
}

int returned(int a, int b) {
    if (a) {
        return a;
    } else
        return b;

    return a + b + a;
}

int loopy(int a, int b) {
    if (a) {
        return 1;
    }

    while (b) {
        b++;
    }

    /* Whitebox: Corner case, for loops are parsed manually. b should not be
       counted here but only a below. */
    for (;;) {
        b++;
    }
    for (;; (b++))
        b++;

    for (b = 0;;) {
        b++;
    }
    for (; a;) {
        return b;
    }
}

int in_condition(int a, int b) {
    int c;
    int d;
    if (a) {
        return a;
    } else {
        return b;
    }

    if (a)
        return c;
    else
        return d;
}

int assignation(int a, int b) {
    if (a = a+b)
        b = a;

    b += 1;
    b -= 1;
    b *= 1;
    b /= 1;
    b &= a;
    b |= a;

    // Read and write expressions
    b++;
    ++b;
    a--;
    --a;

    // Unary operators that should not be counted
    +a;
    -a;
    *a;
    &a;
    __real a;
    __imag a;
    __extension__ a;
}

int arithmetics(int a, int b) {
    // Sum
    a = b + 4;
    a = a + a;
    a += a;
    b -= b;

    // Product
    a = a * b;
    a % b;
    a / b;
    a %= b;
    a /= b;
    a *= b;

    // Binary
    a & b;
    a | b;
    a &= a;
    a |= a;
}

int levels(int first, int second, int third) {
    if (0)
        first = 1;
    else
        if (2) {
            second = 1;
            if (3) {
                third = 2;
            } else
                third = 3;
        }

    if (1) {
        first = 1;
    } else {
        first = 2
    }

    while (1)
        while (1) {
            for(;;)
                third = 3;

            second = 2;
            while (2) {
                third = 5;
            }
        }

    for (;;) {
        first = 1;
    }
}
