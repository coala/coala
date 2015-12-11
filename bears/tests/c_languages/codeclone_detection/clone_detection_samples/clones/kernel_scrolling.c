#include <kernel_print.h>

// Don't do anything if the include fails!
#ifdef BLANK

void clearScreen() {
    uint16_t i;
    volatile unsigned char *videoram = (unsigned char *)FB_MEM_LOCATION;
    for(i=0; i<25*80*2; i++)
        if(i % 2)
            videoram[i]=COLCODE(STDFG, STDBG);
        else
            videoram[i]=BLANK;
    setCursor(GET_POS(0,0));
}

static void scrollUp() {
    uint16_t i;
    volatile unsigned char *videoram = (unsigned char *)FB_MEM_LOCATION;
    for(i=0; i<(FB_LINES-1)*FB_COLUMNS*2; i++)
        videoram[i]=videoram[i+(FB_COLUMNS * 2)];

    for(; i<FB_LINES*FB_COLUMNS*2; i++)
        if(i % 2)
            videoram[i]=COLCODE(STDFG, STDBG);
        else
            videoram[i]=BLANK;
}

#endif
