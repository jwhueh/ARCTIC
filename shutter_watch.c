// Compile with gcc evgpioctl.c -o evgpioctl evgpio.c -mcpu=arm9

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <termios.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>

#include "evgpio.h"

void print_csv(int dio, int value)
{
	printf("%d,%d\n", dio, value);
	fflush(stdout);
}

int main(){
 int opt_watch = 0;
 //       int c, i;

        evgpioinit();

        if(!opt_watch) return 0;
        
        evclrwatch();
        while(1) {
                evwatchin(print_csv);
        }



}


int loop(){
	int opt_watch = 0;

        evgpioinit();

        if(!opt_watch) return 0;

        evclrwatch();
        while(1) {
                evwatchin(print_csv);
        }
}


