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
char buffer[80];

void print_csv(int dio, int value)
{
	//printf("%d,%d\n", dio, value);
	//fflush(stdout);
	pinval = evgetin(dio);
	pin = dio;
}

int getVal(int dio){
        evgpioinit();
        int value = evgetin(dio);
        return value;
} 

int loop(int dio){
        FILE *file;
	time_t rawtime;
	time(&rawtime); struct tm *timeinfo = localtime(&rawtime);
	strftime(buffer,80,"%Y%m%d.log", timeinfo);
	file = fopen((buffer),"a+");
	evgpioinit();
        evclrwatch();
        int waiting = 0;
	int returnVal;
	char *process;
	while(waiting < 1){
		evwatchin(print_csv);
		if(dio == 33){
			waiting = 1;
			event_t = time(NULL);
			if(pinval == 1){
				process = "opening";
			}
			else{
				process = "closing";
			}
			returnVal = pinval;
		}
		else if(dio == pin){
			waiting = 1;
			event_t = time(NULL);
			process = "moving";
			returnVal = event_t;
		}
	}
	fprintf(file,"%d\t%s\t",(int)event_t,process);
	int x;
	for(x=25; x<34; x++) {
		fprintf(file,"%d\t",getVal((int)x));
	}
	fprintf(file,"\n");
	fclose(file);
	return returnVal;
}
