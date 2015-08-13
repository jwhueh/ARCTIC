// Compile with gcc shutter_calibrate.c -o shutter_cablibrate evgpio.c -mcpu=arm9
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

static int right_shutter = 76;
static int left_shutter = 77;
struct timeval first;
struct timeval second;
static int pin;
static int pinval;

void print_csv(int dio, int value)
{
        printf("%d,%d\n", dio, value);
        fflush(stdout);
	pin = dio;
	pinval = value;
}

void moveShutter(int shutter){
	printf("in moveShutter\n");
	int current_value = evgetin(shutter);
	int next_value;
	int waiting = 0;
	if(current_value == 1){
		next_value = 0;
	}else{
		next_value = 1;
	}
	printf("done setting current and next value\n");
	
	if(shutter == right_shutter){
		evsetdata(left_shutter,0);
		sleep(1);
		evsetdata(shutter,next_value);
		while(waiting < 2){
			evwatchin(print_csv);
			if((pin == 26 || pin == 27) && pinval == 0 && waiting == 0){					
				gettimeofday(&first,NULL);
				waiting++;
			}else if((pin == 26 || pin == 27) && pinval == 0 && waiting == 1){
				gettimeofday(&second,NULL);
				waiting++;
			}
		}
		printf("right shutter to %d\n",next_value);
	}else if(shutter == left_shutter){
		evsetdata(right_shutter,1);
		sleep(0);
		evsetdata(shutter,next_value);
                while(waiting < 2){
                	evwatchin(print_csv);
                	if((pin == 30 || pin == 31) && pinval == 0 && waiting == 0){
                		gettimeofday(&first,NULL);
                		waiting++;
                	}else if((pin == 30 || pin == 31) && pinval == 0 && waiting == 1){
                		gettimeofday(&second,NULL);
               			waiting++;
			}	
                }
        	printf("left shutter to %d\n",next_value);
	}else {
		printf("something went wrong");
	} 

	uint64_t first_sec = first.tv_sec;
	uint64_t first_usec = first.tv_usec;
	uint64_t second_sec = second.tv_sec;
	uint64_t second_usec = second.tv_usec;
	double diff_sec = (double)second.tv_sec - (double)first.tv_sec;
	double diff_usec = (double)second.tv_usec/1000000.0 - (double)first.tv_usec/1000000.0;
	double total_diff = diff_sec + diff_usec;
	printf("%lf\n",total_diff);
}


//give the shutter pin you want to move
int main() {
	evgpioinit(); 
        evclrwatch();
	evsetdata(right_shutter,0);
	evsetdata(left_shutter,0);
	printf("right shutter is at %d\n",evgetin(right_shutter));
	printf("left shutter is at %d\n",evgetin(left_shutter));
	int shutter;
	while(1){
		char userinput[80]; 
		printf("left or right? ");
		scanf("%s",userinput);
		if(strcmp(userinput,"left") == 0){
			shutter = 77;
		}
		else if(strcmp(userinput,"right") == 0){
			shutter = 76;
		}
		moveShutter(shutter);
	}
}
