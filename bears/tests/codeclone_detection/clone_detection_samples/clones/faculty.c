int faculty1(int x) {
    int result = x;
    while(x > 2) {
        result *= --x;
    }

    return result;
}

int faculty2(int x) {
    int result = x;
    for(x--; x > 1; --x) {
        result *= x;
    }

    return result;
}
