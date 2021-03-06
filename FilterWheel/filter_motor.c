/**
Author: Joseph Huehnerhoff
Date Created: 2015-09-15
Purpose: Control Arcus stepper driver for ARCTIC filter wheel

usage: gcc -o filter_motor filter_motor.c ArcusPerformaxDriver.c evgpio.c -lusb-1.0 -mcpu=arm9

changelog:
2015-10-28	added comments

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
int setup();
int currentPos();
int motorOn();
int motorOff();
int zero();
int moveMotor(char* mv);
int moveToFilter(int pos, int delta);

/*main function to run the filter wheel from the command line */
int main(int argc, char *argv[])
{
    memset(out,0,64);
    memset(in,0,64);

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
		case 'z':
		    zero();
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
                    break;
		case 'f':
                    printf("%s\n", argv[2]);
                    moveToFilter(atoi(argv[2]), atoi(argv[3]));
                    break;
		}
       	     }
	return 1;
}

/* read in and print the digital input pins */
void print_csv(int dio, int value){
        printf("%d,%d\n", dio, value);
        fflush(stdout);
        pinval = evgetin(dio);
        pin = dio;
}


/* Move the motor to absolute encoder position. */
int moveMotor(char *mv){
	motorOn();


	strcpy(out, "CLR"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }
	
	
	char cmd[12] = "X";  //Setup the Axes to move, this is a single axis controlled so it will always be x

	strcat(cmd, mv);
        strcpy(out, cmd); //move the motor
                if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
                {
                        printf("Could not send\n");
                        return -1;
                 }      
	return 1;
}



/* Stop motor at current location but decelerate in a safe manner */
int stopMotor(){
        strcpy(out, "STOP");
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }       
        return 1;
}

/* Return the state of the motor driver.  
	Return:
		1 - driver power on
		0 - driver power off
*/
int driverStatus(){
	strcpy(out, "EO");
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
	//printf("motor power: %s\n", in);
	return atoi(in);
}

/* Return motor status
	Return - bit value determined from:
	http://staff.washington.edu/jwhueh/ARCTIC/filter/ACE-SDE_Manual_Rev_1.22.pdf
	page 28, table 6.5, also copied below
bit	description
0 	Motor running at constant speed
1 	Motor in acceleration
2 	Motor in deceleration
3	 Home input switch status
4 	Minus limit input switch status
5 	Plus limit input switch status
6 	Minus limit error. This bit is latched when minus limit is hit during motion. This error must be cleared using the CLR command before issuing any subsequent move commands.
7	 Plus limit error. This bit is latched when plus limit is hit during motion. This error must be cleared using the CLR command before issuing any subsequent move commands.
8 	Latch input status
9 	Z-index status
10 	TOC time-out status 
*/
int motorStatus(){
        strcpy(out, "MST");
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
        return atoi(in);
}

/*
moves to filter posional number [0-5]
returns the desired encoder position
*/
int moveToFilter(int pos, int delta){
	int posArr[6]={};

	//populate array with filter encoder positions
	int x;
	for (x=0; x<6; x++) { 
		posArr[x] = delta * x;
	}

	if (pos > sizeof(posArr)/sizeof(int)){
		return -1;
	}

	char mv[12];
	
	sprintf(mv, "%d", posArr[pos]);
	moveMotor(mv);
	return posArr[pos];
}

int currentEnc(){
	/* return current position as determined by the motor encoder */

	strcpy(out, "EX");
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }
        //printf("EX: %s\n",in);
	return atoi(in);
}

int currentPos(){
        /* return current position as determined by the motor encoder */
        strcpy(out, "PX");//change back to EX when working properly
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }
        //printf("EX: %s\n",in);
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
	printf("Step Value Set to 0\n");


	strcpy(out, "EX=0");
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

        return 1;
}



int setVelocity(){
	/* set the speed and ramp parameters
	*Low Speed and high speed define the path generation velocity.  
	*Weird things can heppen if they are really high (motor stalls kinda).
	*/
	
	strcpy(out, "LSPD=300"); //was 20000
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        strcpy(out, "HSPD=500"); //set high speed (original value 10000, 30000)
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        strcpy(out, "ACC=10"); //set acceleration (original value 300)
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

       sleep(.1);
        
        strcpy(out, "LSPD"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {       
                printf("Could not send\n");
                return 1;
        }
        sleep(.11);
        printf("LSPD: %s\n",in);
        
        strcpy(out, "HSPD"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {       
                printf("Could not send\n");
                return 1;
        }
        sleep(.11);
        printf("HSPD: %s\n",in);
        

	return 1;
}

int homeVelocity(){
	 /* set the speed and ramp parameters
        *Low Speed and high speed define the path generation velocity.
        *Weird things can heppen if they are really high (motor stalls kinda).
        */
	
        strcpy(out, "LSPD=10"); //set low speed (original value 1000)
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        strcpy(out, "HSPD=50"); //set high speed (original value 10000)
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

int closeConnection(){
        memset(out,0,64);
        memset(in,0,64);
         if(!fnPerformaxComClose(Handle))
        {
                printf( "Error opening device\n");
                return 1;
        }
	return 1;
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
                return -1;
        }
        if(num<1)
        {
                printf( "No motor found\n");
                return -1;
        }

        if(!fnPerformaxComOpen(0,&Handle))
        {
                printf( "Error opening device\n");
                return -1;
        }

        if(!fnPerformaxComSetTimeouts(500,500))
        {
                printf("Error setting timeouts\n");
                return -1;
        }
        if(!fnPerformaxComFlush(Handle))
        {
                printf("Error flushing the coms\n");
                return -1;
        }

	printf("Setting Up Device\n");

	/* return the motor information */
        strcpy(out, "ID"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {       
                printf("Could not send\n");
                return -1;
        }
        
        printf("Arcus Product: %s\n",in);
        
        strcpy(out, "DN"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {       
                printf("Could not send\n");
                return -1;
        }
        
        printf("Device Number: %s\n",in);
        
        strcpy(out, "ABS"); //read current 
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {       
                printf("Could not send\n");
                return -1;
        }
        
        printf("Set move mode to absolute: %s\n",in);
        
        
        strcpy(out, "DOBOOT=0"); //read current 
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {       
                printf("Could not send\n");
                return -1;
        }
        
        printf("Disable Output, DOBOOT: %s\n",in);
        
        
        strcpy(out, "EDIO=0"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {       
                printf("Could not send\n");
                return -1;
        }
        
        printf("Disable DIO, EDIO: %s\n",in);

 	strcpy(out, "POL=4"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }

        printf("Set Limit Polarity: %s\n",in);

                strcpy(out, "POL=6"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }

        printf("Set Latch Polarity: %s\n",in);

        strcpy(out, "POL=1"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }

        printf("Set Directional Polarity: %s\n",in);


        strcpy(out, "SCV=0"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }

        printf("S-Curve Ramp Enabled: %s\n",in);



        strcpy(out, "IERR=1"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }

        printf("Ignore Error Enabled: %s\n",in);

	strcpy(out, "MST"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }

        printf("Motor Status, MST: %s\n",in);



        strcpy(out, "RR"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }
        sleep(2.5);//RR requires a 2 second minimum
        printf("Read Drive Parameters, RR: %s\n",in);

        strcpy(out, "DRVRC=1500"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }
        sleep(.1);
        printf("Set Drive Current, 1.5A, DRVRC: %s\n",in);


        strcpy(out, "RW"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }

	printf("Write Motor Parameters, RW: %s\n",in);


        sleep(1);
        strcpy(out, "SL=1"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }       
        
        printf("Write SL Parameters, SNL: %s\n",in);


	 sleep(1);

        strcpy(out, "SLR=25"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }       

        printf("Write SNL Parameters, SNL: %s\n",in);


        sleep(2.5);

        strcpy(out, "CLR"); //read current
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }
        printf("Clear Errors: %s\n",in);
	setVelocity();

	return 1;	
}
