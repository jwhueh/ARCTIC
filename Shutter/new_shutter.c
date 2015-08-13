// Compile with gcc new_shutter.c -o new_shutter evgpio.c -mcpu=arm9
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

char buffer[80];
static int pin;
static int pinval;
static int right;
struct timeval start_exp;
struct timeval end_exp;
static int lookingfor = 0;
static int found = 0;

void print_csv(int dio, int value){
        printf("%d,%d\n", dio, value);
        fflush(stdout);
        pinval = evgetin(dio);
        pin = dio;
}

int homeStatus(){
        int statusval;
        if(evgetin(28) == 0 && evgetin(29) == 0){
                statusval = 1; 
                right = 1;
        }else{  
                statusval = 0;
                right = 0;
        }       
	return statusval;
}

void move() {
	found = 0;
	if(pinval == 0){
		if(right == 1){
			evsetdata(77,1);
			printf("moving left shutter right");
		}else{
			evsetdata(76,0);
			printf("moving right shutter left");
		}
	} else{
		lookingfor = 0;
		int status = homeStatus();
		if(status == 1){
			evsetdata(76,1);
			printf("moving right shutter right");
		}else{
			evsetdata(77,0);
			printf("moving left shutter left");
		}
	}
}

void expTime(){
	if(lookingfor == 0){
		gettimeofday(&start_exp,NULL);
		if(pin == 26){
			lookingfor = 31;
			printf("saw pin %d, looking for pin %d\n",pin,lookingfor);
		}else if(pin == 30){
			lookingfor = 27;
			printf("saw pin %d, looking for pin %d\n",pin,lookingfor);
		}else if(pin == 27){
			lookingfor = 30;
			printf("saw pin %d, looking for pin %d\n",pin,lookingfor);
		}else if(pin == 31){
			lookingfor = 26;
			printf("saw pin %d, looking for pin %d\n",pin,lookingfor);
		}
	}else if (pin == lookingfor){
		gettimeofday(&end_exp,NULL);
		lookingfor = 0;
		double diff = (end_exp.tv_sec - start_exp.tv_sec) + (end_exp.tv_usec-start_exp.tv_usec)/100000.0;
		printf("%f\t%f\n",(double)(end_exp.tv_sec - start_exp.tv_sec), (double)(end_exp.tv_usec-start_exp.tv_usec));
		printf("exposure time = %f\n", diff);
		FILE *file;
		file = fopen((buffer),"a+");
		fprintf(file,"%f\n", diff);
		fclose(file);
		found = 2;
	}
	
}

int main(){

	//c version of startup.bash for initialization
	evgpioinit();
	evsetdata(76,0);
	evsetdata(77,0);
	evsetdata(61,0);
	int i;
	for(i=0;i<128;i++){
		evsetmask(i,1);
	}
	for(i=25;i<34;i++){
		evsetmask(i,1);
		evgetin(i);
	}
	sleep(2);
        evclrwatch();
	while(1){
		evwatchin(print_csv);
		if(pin == 33){
			move();
		}else if((pin == 26 || pin == 27 || pin == 30 || pin == 31) && pinval == 0 && found < 2){
			expTime();
		}
		time_t rawtime;
        	time(&rawtime); struct tm *timeinfo = localtime(&rawtime);
        	struct timeval now;
		strftime(buffer,80,"%Y%m%d.logfile", timeinfo);
		gettimeofday(&now, NULL);
                uint64_t event_sec = now.tv_sec;
                uint64_t event_usec = now.tv_usec;
                FILE *file;
                file = fopen((buffer),"a+");
                fprintf(file,"%llu.%llu\t",(long long unsigned) event_sec, (long long unsigned) event_usec);
                int x;
                for(x=25; x<34; x++) {
                        int value = evgetin((int)x);
                        fprintf(file,"%d\t",value);
                }
                fprintf(file,"\n");
                fclose(file);
		
	}	
}

