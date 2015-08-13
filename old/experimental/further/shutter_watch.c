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

struct pinInfo_t{
	int dio;
	int value; 
};

int getVal(int dio){
        evgpioinit();
        int value = evgetin(dio);
        return value;
}

void loop(void(*callback)(struct pinInfo_t *)){
        FILE *file;
	time_t rawtime;
	time(&rawtime); struct tm *timeinfo = localtime(&rawtime);
	strftime(buffer,80,"%Y%m%d.log", timeinfo);
	file = fopen((buffer),"a+");
	evgpioinit();
        evclrwatch();
	evwatchin(print_csv);
	fprintf(file,"%s\t",buffer);
	int x;
	for(x=25; x<34; x++) {
		fprintf(file,"%d\t",getVal((int)x));
	}
	struct pinInfo_t info;
	info.dio = pin;
	info.value = pinval;
	callback(&info);
	fprintf(file,"\n");
	fclose(file);
	
	return;
}
