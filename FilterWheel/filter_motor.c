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

int main(int argc, char *argv[])
{

    /*display arguments, used for testing*/
    int i = 0;
    for (i = 0; i < argc; i++) {
    printf("argv[%d] = %s\n", i, argv[i]);
    }

    memset(out,0,64);
    memset(in,0,64);

    int index;
    int c;

    setup(); //start the communications

    while ((c = getopt (argc, argv, "epmtoz")) != -1)
        switch (c)
	    {
	    if(argc==1){
	        case 'e':
        	    exercise(); 
		    break;

	        case 'p':
		    currentPos();
		    break;

	        case 't':
		    printf("test\n");
	  	    break;
		case 'o':
		    turnOff();
		    break;
		case 'z':
		    home();
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
		}
       	     }
}

int moveMotor(char *mv){
	strcpy(out, "EO=1"); //enable device
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
	

	char cmd[12] = "X";  //Setup the Axes to move, this is a single axis controlled so it will always be x

        strcat(cmd, mv);
        strcpy(out, cmd); //move the motor
                if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
                {
                        printf("Could not send\n");
                        return 1;
                 }      
	/* check the motor position and make sure it completes a move
	* should probably add some error checking at some point
	*/
        while(strcmp(mv, in)!=0){
        strcpy(out, "PX");
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
                {
                        printf("Could not send\n");
                        return 1;
                 }
        printf ("Position: %s, Move: %s\n", in, mv); //this can be removed in final version
        sleep(1);
        }
	strcpy(out, "EO=0"); //enable device
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

	return 1;
}


int exercise(){
	/* move the motor around to make sure everything is working */
	printf("Motor is moving. Please wait.\n");

        char mv[12] = "20000";
	moveMotor(mv);

        char mn[12] = "-20000";
	moveMotor(mn);

	return 1;
}

int currentPos(){
	/* return current position as determined by the motor encoder */
	strcpy(out, "PX");
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
        printf("Current Encoder Value: %s\n",in);
	return 1;
}

int home(){
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

int turnOff(){
	/* Turn off motor current */
	strcpy(out, "EO=0"); //enable device
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }      

	sleep(1);
	strcpy(out, "EO"); //enable device
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
	printf("Motor State is %s\n",in);

	return 1;
}

int turnOn(){
        /* Turn off motor current */
        strcpy(out, "EO=1"); //enable device
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        sleep(1);
        strcpy(out, "EO"); //enable device
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
        printf("Motor State is %s\n",in);

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

        strcpy(out, "LSPD=10000"); //set low speed (original value 1000)
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        strcpy(out, "HSPD=40000"); //set high speed (original value 10000)
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        strcpy(out, "ACC=300"); //set acceleration (original value 300)
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
	return 1;
}


int setup(){
	/* setup communications to the device */
	memset(out,0,64);
        memset(in,0,64);


	/* setup gpio */

	/*evgpioinit();
        evsetddr(81,0);
        evsetddr(82,0);
	evsetddr(83,1);
        evsetdata(61,0);
        int i;
        for(i=36;i<41;i++){
                evsetmask(i,1);
                evgetin(i);
        }
        sleep(1);
        evclrwatch();
	*/
	/* current values */
	/*
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

        printf("Clear Errors: %s\n",in);
	setVelocity();
	info();
}
