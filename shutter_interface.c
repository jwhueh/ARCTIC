/* File : shutter.c */

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

/*int main(int argc, char **argv)
{
	int c;
	int fact(int n);

	while((c = getopt(argc, argv, "i:s")) != -1) {
		int dio;
		switch(c) {
		case 'i':
			dio = atoi(optarg);
			//printf("dio%d=%d\n", dio, evgetin(dio));
			printf("%d", dio);
			break;
		case 's':
			fact(2);
			break;
		}
	}	
	return 1;
}*/

/* Compute factorial of n */
int  fact(int n) {
	printf ("%d", n);
	if (n <= 1) return 1;
	else return n*fact(n-1);
}


void moveShutter(int pin, int pos){
	printf ("%d, %d", pin, pos);
	evsetdata(pin,pos);
	return;
}

void openConnection(){
	evgpioinit();
	//add any odd setup stuff here
	return;
}

void print_csv(int dio, int value)
{
        printf("%d,%d\n", dio, value);
        fflush(stdout);
}

void leachMonitor(int condition){
        printf("entered leachMonitor");
        evclrwatch();
        while(condition == 1) {
            evwatchin(print_csv);
            printf ("running evwatchin");
        }
        return;
}

void closeConnection(int pin, int pos){
	printf ("%d, %d", pin, pos);
	return;
}

void shutterStatus(){

	return;
}

