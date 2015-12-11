#include <stdint.h>

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

char errMessage[MAX_ERRNO][27] =
{
	"Unknown error code!",
	"Yet unimplemented feature!",
	"Unsupported architecture!",
	"Out of range!",
	"Object already exists!",
	"A subroutine failed!"
};

char * getErrText(const err_t errCode)
{
	if(errCode != SUCCESS)
	{
		if(ABS(errCode) < MAX_ERRNO)
		{
			return errMessage[ABS(errCode)];
		}
		return errMessage[0];
	}
	return "Function executed successfully.";
}

extern inline bool assertSuccess(const err_t errCode)
{
	if(errCode != SUCCESS)
	{
		//will halt the kernel, no return needed
		fatalErr("%s", getErrText(errCode));
	}
	return true;
}
