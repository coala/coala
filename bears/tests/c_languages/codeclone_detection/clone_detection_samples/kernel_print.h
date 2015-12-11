#include <stdint.h>

#define BLANK   ' '

#define STDBG   T_BLUE
#define STDFG   T_WHITE
#define STDCOL  COLCODE(STDFG, STDBG)

//color
#define T_BLACK     0
#define T_BLUE      1
#define T_GREEN     2
#define T_CYAN      3
#define T_RED       4
#define T_MAGENTA   5
#define T_BROWN     6
#define T_LIGHTGRAY 7
#define T_WHITE     T_LIGHT(T_LIGHTGRAY)

#define COLCODE(fore, back) (((back)<<4) + (fore))

#define T_LIGHT(col)    ((col)+0x8)

#define GET_POS(x,y)    ((y)*80 + (x))

#define FB_LINES    25
#define FB_COLUMNS  80

#define FB_MEM_LOCATION 0xB8000
