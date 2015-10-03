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
int setup();
int currentPos();
int motorOn();
int motorOff();
int readConfig();
int zero();
int home();
int moveMotor(char* mv);
int moveToFilter(int pos);
int findHysteresis();




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
                    break;
		case 'f':
                    printf("%s\n", argv[2]);
                    moveToFilter(atoi(argv[2]));
                    break;
		}
       	     }
	return 1;
}

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

	strcpy(out, "CLR"); //read current
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
                        return -1;
                 }      
//	motorOff();
	return 1;
}

int stopMotor(){
        strcpy(out, "STOP");
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return -1;
        }       
        return 1;
}

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

int motorStatus(){
        strcpy(out, "MST");
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
        return atoi(in);

}

int moveToFilter(int pos){
	/*
	moves to filter posional number [0-5]
	returns the desired encoder position
	*/

	int incmv = 33800; //this should be read in from config file
	int posArr[6]={};

	//populate array with filter encoder positions
	int x;
	for (x=0; x<6; x++) { 
		posArr[x] = incmv * x;
	}

	if (pos > sizeof(posArr)/sizeof(int)){
		return -1;
	}

	char mv[12];
	
	sprintf(mv, "%d", posArr[pos]);
	moveMotor(mv);
	return posArr[pos];
}

int filterPos(){
	int pos = currentPos();
	int incmv = 33800;
	int fw = pos/incmv;
	return fw;
}

int currentEnc(){
	/* return current position as determined by the motor encoder */
	strcpy(out, "EX");//change back to EX when working properly
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
	sleep(.1);
	strcpy(out, "EO"); //enable device
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
	//printf("Motor State is %s\n",in);
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

	        strcpy(out, "EO"); //enable device
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }
        //printf("Motor State is %s\n",in);

        return 1;
}



int setVelocity(){
	/* set the speed and ramp parameters
	*Low Speed and high speed define the path generation velocity.  
	*Weird things can heppen if they are really high (motor stalls kinda).
	*/
	
       // strcpy(out, "LSPD=5000"); //set low speed (original value 1000)
	strcpy(out, "LSPD=20000");
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        strcpy(out, "HSPD=30000"); //set high speed (original value 10000)
	//strcpy(out, "HSPD=100000");
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
        strcpy(out, "LSPD=300"); //set low speed (original value 1000)
        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
        {
                printf("Could not send\n");
                return 1;
        }

        strcpy(out, "HSPD=1000"); //set high speed (original value 10000)
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
	printf("Starting Home Routine.\nMoving till home sensors detected.\n");
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
			printf("Near home position detected\n");
			sleep(1);
			
			printf("Starting slow home.\n");
			homeVelocity();
			findHysteresis();
		
	
			sleep(1);
			//readConfig();	
			
			moveMotor("700");
			sleep(2);
			zero();	
			printf("Zeropoint found, Detecting FW ID.\n");

			moveMotor("-500");  //move to trigger point
			sleep(3);
			//read ID
			int x;
                        char idi[4];
                        char  v[1];
                        for(x=37; x<40; x++) {
                        int value = evgetin((int)x);
                        printf("%d\t",value);
                        if (value == 0){
                                        strcpy(v,"1");
                                } else{
                                        strcpy(v,"0");
                                }
                                strcat(idi, v);
                        }
                                printf("\n");


			sleep(.1);
			printf("Moving to 0.\n");
			moveMotor("0");
			sleep(3);

			setVelocity();
			printf("Current Position: ");
			printf("%d\n", currentPos());
			printf("ID:%s\n",idi);
			return atoi(idi);      
                 }
		}
        return -1;
} 

int findHysteresis(){
	// change this code to use the current position paramter
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
	int y;
	for (y=0;y<3;y++){	
        	evwatchin(print_csv);
		int x;
		 for(x=37; x<40; x++) {
                        int value = evgetin((int)x);
                        printf("%d\t",value);
                }
                printf("\n");

                if(pin == 39 || pin == 38 || pin == 37){
			strcpy(out, "STOP");
                        if(!fnPerformaxComSendRecv(Handle, out, 64,64, in))
                        {
                                printf("Could not send\n");
                                return 1;
                        }
			return 1;
                	}

		}
	return -1;
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


        strcpy(out, "SCV=1"); //read current
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
