// From CPython: https://hg.python.org/cpython

// Dummies
#define Py_CHARMASK(c) c
#define Py_ISLOWER(c) c
#define Py_TOLOWER(c) c
#define Py_ISUPPER(c) c
#define Py_TOUPPER(c) c
#define PyBool_FromLong(c) c
typedef int Py_ssize_t;
typedef int PyObject;
#define Py_RETURN_FALSE 1

PyObject*
_Py_bytes_islower(const char *cptr, Py_ssize_t len)
{
    const unsigned char *p
        = (unsigned char *) cptr;
    const unsigned char *e;
    int cased;

    /* Shortcut for single character strings */
    if (len == 1)
        return PyBool_FromLong(Py_ISLOWER(*p));

    /* Special case for empty strings */
    if (len == 0)
        Py_RETURN_FALSE;

    e = p + len;
    cased = 0;
    for (; p < e; p++) {
        if (Py_ISUPPER(*p))
            Py_RETURN_FALSE;
        else if (!cased && Py_ISLOWER(*p))
            cased = 1;
    }
    return PyBool_FromLong(cased);
}

PyObject*
_Py_bytes_isupper(const char *cptr, Py_ssize_t len)
{
    const unsigned char *p
        = (unsigned char *) cptr;
    const unsigned char *e;
    int cased;

    /* Shortcut for single character strings */
    if (len == 1)
        return PyBool_FromLong(Py_ISUPPER(*p));

    /* Special case for empty strings */
    if (len == 0)
        Py_RETURN_FALSE;

    e = p + len;
    cased = 0;
    for (; p < e; p++) {
        if (Py_ISLOWER(*p))
            Py_RETURN_FALSE;
        else if (!cased && Py_ISUPPER(*p))
            cased = 1;
    }
    return PyBool_FromLong(cased);
}
