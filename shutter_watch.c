// Compile with gcc evgpioctl.c -o evgpioctl evgpio.c -mcpu=arm9
#include <time.h>
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

static int pinval;
static int pin;
static time_t event_t;

void print_csv(int dio, int value)
{
	//printf("%d,%d\n", dio, value);
	//fflush(stdout);
	pinval = evgetin(dio);
	pin = dio;
}

int loop(int dio){
        evgpioinit();
        evclrwatch();
        int waiting = 0;
	while(waiting < 1){
		evwatchin(print_csv);
		if(dio == 33){
			waiting = 1;
			return pinval;
		}
		else if(dio == pin){
			waiting = 1;
			event_t = (int)time(NULL);
			return event_t;
		}
	}
}

int getVal(int dio){
	evgpioinit();
	int value = evgetin(dio);
	return value;
}
