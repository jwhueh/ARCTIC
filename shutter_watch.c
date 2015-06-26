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
	printf("%d,%d\n", dio, value);
	fflush(stdout);
	pinval = evgetin(dio);
	pin = dio;
}

int loop(){
	//int opt_watch = 1;
        evgpioinit();

        //if(!opt_watch) return 0;
	
        evclrwatch();
        evwatchin(print_csv);
	return pinval;
}


/*double loop(int dio){
        evgpioinit();
        evclrwatch();
        int waiting = 0;
	while(waiting < 1){
		evwatchin(print_csv);
		if(dio == 33){
			waiting = 1;
			//double pinval_d = (double)pinval;
			//return pinval_d;
			return pinval;
		}
		else if(dio == pin){
			waiting = 1;
			event_t = time(NULL);
			return event_t;
		}
	}
}*/

int getVal(int dio){
	evgpioinit();
	int value = evgetin(dio);
	return value;
}

double timing(int dio){
	evgpioinit();
        evclrwatch();
	int passed = 0;
	while(passed < 1){
            evwatchin(print_csv);
	    if(pin == dio){
	        event_t = time(NULL);
		passed = 1;
	    }
	}		
	return event_t;
}
