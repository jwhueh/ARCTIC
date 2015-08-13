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
char* arr[20];

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

char* loop(int dio){
        time_t rawtime;
        time(&rawtime); struct tm *timeinfo = localtime(&rawtime);
        struct timeval now;
        strftime(buffer,80,"%Y%m%d.log", timeinfo);
        evgpioinit();
        evclrwatch();
        int waiting = 0;
        //char *process;
	char* arr=malloc(1024);
	
        while(waiting < 1){
		arr[20] = "";
		char v[20];
                evwatchin(print_csv);
                if(pin == 33){
                        waiting = 1;
                }
        	gettimeofday(&now, NULL);
        	uint64_t event_sec = now.tv_sec;
        	uint64_t event_usec = now.tv_usec;
        	FILE *file;
		file = fopen((buffer),"a+");
		fprintf(file,"%llu.%llu\t",(long long unsigned int) event_sec, (long long unsigned int) event_usec);
        	int x;
		strcpy(arr,"");
        	for(x=25; x<34; x++) {
			int value = getVal((int)x);
                	fprintf(file,"%d\t",value);
			sprintf(v,"%d",value);
			strcat(arr,v);
        	}
        	fprintf(file,"\n");
		printf("buffer: %s\n",arr);
		fclose(file);
        }
        return arr;
}
