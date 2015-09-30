/**

gcc -o filter_motor filter_motor.c ArcusPerformaxDriver.c evgpio.c -lusb-1.0 -mcpu=arm9

**/
#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include "ArcusPerformaxDriver.h"



char            lpDeviceString[PERFORMAX_MAX_DEVICE_STRLEN];
AR_HANDLE       Handle; //usb handle
char            out[64];
char            in[64];
AR_DWORD        num;
int i;
static int pin;
static int pinval;

/*int main(int argc, char *argv[])
{


    memset(out,0,64);
    memset(in,0,64);

    int index;
    int c;

    setup(); //start the communications

    while ((c = getopt (argc, argv, "pmftoiczh")) != -1)
        switch (c)
	    {
	    if(argc==1){
	        case 'p':
		    currentPos();
		    break;
	        case 't':
		    printf("test\n");
	  	    break;
		case 'o':
		    motorOff();
		    break;
		case 'c':
		    readConfig();
		    break;
		case 'z':
		    zero();
		    break;
		case 'h':;
                    int retStr = home();
		    printf("Filter ID: %d\n", retStr);
                    break;
		case '?':
         	    if (isprint (optopt))
           	        fprintf (stderr, "Unknown option `-%c'.\n", optopt);
         	    else
           		fprintf (stderr,
                        "Unknown option character `\\x%x'.\n",
                        optopt);
			return 1;
       			default:
         		abort ();
	    }
	    if(argc==2){
		case 'm':
                    printf("%s\n", argv[2]);
                    moveMotor(argv[2]);
		    return;
                    break;
		case 'f':
                    printf("%s\n", argv[2]);
                    moveToFilter(atoi(argv[2]));
                    return;
                    break;
	
		}
       	     }
}*/

void print_csv(int dio, int value){
        printf("%d,%d\n", dio, value);
        fflush(stdout);
        pinval = evgetin(dio);
        pin = dio;
}

int moveMotor(char *mv){
	/*
	Move the motor to absolute encoder position.
	*/

	motorOn();
	char cmd[12] = "X";  //Setup the Axes to move, this is a single axis controlled so it will always be x

        strcat(cmd, mv);
        strcpy(out, cmd); //move the motor
                if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
                {
                        printf("Could not send\n");
                        return -1;
                 }      
	motorOff();
	return 1;
}

int motorStatus(){
	strcpy(out, "EO");
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
        //printf("Motor Driver Status: %s\n",in);
	return atoi(in);

}

int moveToFilter(int pos){
	strcpy(out, "PX");
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

	int incmv = 34140;

	int cF = atoi(in) / incmv;

	int toMove = pos - cF;
	printf("current position: %d, desired position: %d, filter positions to move: %d\n", cF, pos, toMove);
	

	int pxmv = incmv*toMove +atoi(in);

	printf("encoder steps to move: %d\n", pxmv);

	char c[20];

	sprintf(c, "%d", pxmv);
	moveMotor(c);

	return 1;
}


int currentPos(){
	/* return current position as determined by the motor encoder */
	strcpy(out, "PX");
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }
        //printf("%s\n",in);
	return atoi(in);
}

int zero(){
        /* return current position as determined by the motor encoder */
        strcpy(out, "PX=0");
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
	printf("Encoder Value Set to 0\n");
	
	currentPos();

        return 1;
}

int motorOff(){
	/* Turn OFF motor current */
	strcpy(out, "EO=0"); //enable device
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }      
	/*
	sleep(.1);
	strcpy(out, "EO"); //enable device
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
	printf("Motor State is %s\n",in);
	*/
	return 1;
}

int motorOn(){
        /* Turn ON motor current */
        strcpy(out, "EO=1"); //enable device
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        sleep(.1);
        /*strcpy(out, "EO"); //enable device
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
        printf("Motor State is %s\n",in);*/

        return 1;
}



int info(){
	/* return the motor information */
        strcpy(out, "ID"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        printf("Arcus Product: %s\n",in);

        strcpy(out, "DN"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        printf("Device Number: %s\n",in);

        strcpy(out, "ABS"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        printf("BOOT: %s\n",in);


	strcpy(out, "EDIO=0"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        printf("Device Number: %s\n",in);


        strcpy(out, "POL=1"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        printf("Device Number: %s\n",in);

        strcpy(out, "IERR=1"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        printf("Device Number: %s\n",in);



	return 1;
}

int setVelocity(){
	/* set the speed and ramp parameters
	*Low Speed and high speed define the path generation velocity.  
	*Weird things can heppen if they are really high (motor stalls kinda).
	*/

        strcpy(out, "LSPD=5000"); //set low speed (original value 1000)
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        strcpy(out, "HSPD=30000"); //set high speed (original value 10000)
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        strcpy(out, "ACC=100"); //set acceleration (original value 300)
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
	return 1;
}

int homeVelocity(){
	 /* set the speed and ramp parameters
        *Low Speed and high speed define the path generation velocity.
        *Weird things can heppen if they are really high (motor stalls kinda).
        */

        strcpy(out, "LSPD=1000"); //set low speed (original value 1000)
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        strcpy(out, "HSPD=5000"); //set high speed (original value 10000)
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        strcpy(out, "ACC=50"); //set acceleration (original value 300)
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
        return 1;
}

int readConfig(){

	//char arra[10][100];
	char c[1000];
	char file_name[] = "fw.conf";
   	FILE *fp;
	fp = fopen(file_name,"r"); // read mode
 
   	if( fp == NULL )
   	{
      		perror("Error while opening the file.\n");
      		exit(EXIT_FAILURE);
   	}
 
   	printf("The contents of %s file are :\n", file_name);

	fscanf(fp,"%[^\n]",c);
   	printf("Data from file:\n%s",c);
   	fclose(fp);
 
  	return 0;
	}


int home(){
	strcpy(out, "EO=1"); //enable device
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
        
        strcpy(out, "X410000"); //move the motor
                if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
                {
                        printf("Could not send\n");
                        return 1;
                 }      
                 
        evclrwatch();

        //change this to a timed loop
        while(1){
                evwatchin(print_csv);
                if(pin == 37 || pin == 38 || pin == 39){
			strcpy(out, "STOP");
        		if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
                	{
                        	printf("Could not send\n");
                        	return 1;
                 	}
			sleep(2);
			currentPos();
			sleep(1);
			zero();
			printf("Zeroed near home\n");
			sleep(1);
			findHysteresis();
			sleep(1);
			//readConfig();	
			strcpy(out, "PX=700");  //offset
		        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
                	{
                        	printf("Could not send\n");
                        	return 1;
                 	}
			char idi[4];
			char  v[1];
			int x;
                 	for(x=37; x<40; x++) {
                        	int value = evgetin((int)x);
				if (value == 0){
					strcpy(v,"1");
				} else{
					strcpy(v,"0");
				}
				strcat(idi, v);
			}
			moveMotor("0");
			sleep(1);
			printf("Current Position: ");
			currentPos();
			printf("\n");

			return atoi(idi);      
                 }
		}
        return -1;
} 

int findHysteresis(){
	// change this code to use the current position paramter
	int end = 1;
	motorOn();
	homeVelocity();
	sleep(1);
	strcpy(out, "X-5000"); //move the motor
                if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
                {
                        printf("Could not send\n");
                        return 1;
                 }
	
	evclrwatch();
	while(end){	
        evwatchin(print_csv);
		int x;
		 for(x=36; x<40; x++) {
                        int value = evgetin((int)x);
                        printf("%d\t",value);
                }
                printf("\n");
                if(pin == 39){
			strcpy(out, "STOP");
			end = 0;
                        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
                        {
                                printf("Could not send\n");
                                return 1;
                        }
			sleep(.1);
		}
	}
	printf("negative limit: ");
	currentPos();
        printf("\n");
	sleep(1);

	return 1;
} 

int hallStatus(){
	int x;
	char v[1];
	char hall[] = "";
        for(x=36; x<40; x++) {
        	int value = evgetin((int)x);
                //printf("%d\t",value);
		if (value == 0){
			strcpy(v,"0");
		} else {
			strcpy(v, "1");
		}
		strcat(hall, v);
                }
	return atoi(hall);
	//return 1;	
}


int setup(){
	/* setup communications to the device */
	memset(out,0,64);
        memset(in,0,64);


	/* setup gpio */

	evgpioinit();
        evsetddr(81,0);
        evsetddr(82,0);
	evsetddr(83,1);
        evsetdata(61,0);

	
        int i;
        for(i=36;i<41;i++){
                evsetmask(i,1);
                evgetin(i);
        }

        sleep(.1);
        evclrwatch();
	
	/* current values */
	/* the following needs to be added to the status routine
	int x;
	for(x=36; x<41; x++) {
        	int value = evgetin((int)x);
                printf("%d\t",value);
        }
	printf("\n");
	*/

        if(!fnPerformaxComGetNumDevices(&num))
        {
                printf("error in fnPerformaxComGetNumDevices\n");
                return 1;
        }
        if(num<1)
        {
                printf( "No motor found\n");
                return 1;
        }

        if(!fnPerformaxComOpen(0,&Handle))
        {
                printf( "Error opening device\n");
                return 1;
        }

        if(!fnPerformaxComSetTimeouts(500,500))
        {
                printf("Error setting timeouts\n");
                return 1;
        }
        if(!fnPerformaxComFlush(Handle))
        {
                printf("Error flushing the coms\n");
                return 1;
        }

        strcpy(out, "CLR"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        //printf("Clear Errors: %s\n",in);
	setVelocity();
	//info();
}
