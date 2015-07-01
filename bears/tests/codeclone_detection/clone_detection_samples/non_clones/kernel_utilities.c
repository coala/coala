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
