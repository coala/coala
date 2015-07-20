// From CPython: https://hg.python.org/cpython

// Dummies
#define Py_CHARMASK(c) c
#define Py_ISLOWER(c) c
#define Py_TOLOWER(c) c
#define Py_ISUPPER(c) c
#define Py_TOUPPER(c) c
typedef int Py_ssize_t;

void
_Py_bytes_swapcase(char *result, char *s, Py_ssize_t len)
{
    Py_ssize_t i;

    for (i = 0; i < len; i++) {
        int c = Py_CHARMASK(*s++);
        if (Py_ISLOWER(c)) {
            *result = Py_TOUPPER(c);
        }
        else if (Py_ISUPPER(c)) {
            *result = Py_TOLOWER(c);
        }
        else
            *result = c;
        result++;
    }
}

void
_Py_bytes_capitalize(char *result, char *s, Py_ssize_t len)
{
    Py_ssize_t i;

    if (0 < len) {
        int c = Py_CHARMASK(*s++);
        if (Py_ISLOWER(c))
            *result = Py_TOUPPER(c);
        else
            *result = c;
        result++;
    }
    for (i = 1; i < len; i++) {
        int c = Py_CHARMASK(*s++);
        if (Py_ISUPPER(c))
            *result = Py_TOLOWER(c);
        else
            *result = c;
        result++;
    }
}
