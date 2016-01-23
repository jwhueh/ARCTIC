// Compile with gcc readDI.c -o readDI evgpio.c -mcpu=arm9

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

int main(){
	evgpioinit();
	int x;
	for(x=25; x<34; x++) {
		//int value = 0;
		int value = evgetin((int)x);
		printf("%d\t",value);
	}
	printf("\n");
}
