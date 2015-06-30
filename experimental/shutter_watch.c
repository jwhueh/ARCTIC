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
#include <sys/time.h>

static int pinval;
static int pin;
char buffer[80];
struct timeval now;

void print_csv(int dio, int value)
{
	printf("%d,%d\n", dio, value);
	fflush(stdout);
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
        struct timeval now;
        strftime(buffer,80,"%Y%m%d.log", timeinfo);
        file = fopen((buffer),"a+");
        evgpioinit();
        evclrwatch();
        int waiting = 0;
        //char *process;
        while(waiting < 1){
                evwatchin(print_csv);
                if(pin == 33){
                        waiting = 1;
                }
        	gettimeofday(&now, NULL);
        	uint64_t event_sec = now.tv_sec;
        	uint64_t event_usec = now.tv_usec;
        	fprintf(file,"%llu.%llu\t",(long long unsigned int) event_sec, (long long unsigned int) event_usec);
        	int x;
        	for(x=25; x<34; x++) {
                	fprintf(file,"%d\t",getVal((int)x));
        	}
        	fprintf(file,"\n");
        }
	fclose(file);
        return pinval;
}
