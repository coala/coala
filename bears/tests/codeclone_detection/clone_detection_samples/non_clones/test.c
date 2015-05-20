int faculty(int x) {
    int result = x;
    while(x > 2) {
        result *= --x;
    }

    return result;
}

int power(int x, int y) {
    int result = x;
    for(; y>1; y--) {
        result *= x;
    }

    return result;
}

int add(int x, int y) {
    return x + y;
}

int divide(int x, int y) {
    return x / y;
}

void *memcpy(void *restrict dst, const void *restrict src, int len) {
	char *dt = (char*)dst;
	char *sc = (char*)src;
	while(len--)
		*dt++ = *sc++;
	return dst;
}

void *memset(void * dst, int val, int len) {
	char *dt = (char*)dst;
	while(len--)
		*dt++ = (char)val;
	return dst;
}

char *strcpy(char *restrict dest, const char *restrict src) {
	char * dt = dest;
	while((*dest++ = *src++));
	return dt;
}

int strlen(const char * s) {
	int i;
	for (i = 0; s[i] != '\0'; i++) ;
	return i;
}

int main(void) {
    return faculty(power(5, 8));
}

/*
 * Dumb function that retrieves the minimum of 0 and a given value. However if
 * a is actually zero the creative writer of this function wants the value of
 * a mysterious second parameter to be the returned one in the hope it may
 * be 42!
 */
int min_0_a(int a, int b) {
    if (a != 0) {
        if (a > 0)
            return a;
    } else {
        if (a != 0)
            return b;
    }
}

/*
 * Dumb function that is badly written and returns a second parameter if the
 * first one is smaller than 0, the first one otherwise.
 */
int retval(int a, int b) {
    if (a < 0 && a != 0) {
        return b;
    } else {
        return a;
    }
}

struct test_struct {
    int first;
}

void do_something(struct test_struct *a) {
    do_something(a);
    do_something(a);
}

void initialize(struct test_struct *a) {
    a->first = 2;
    a->second = 2;

    do_something(a);
}
