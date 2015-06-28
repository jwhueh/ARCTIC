// Arcus.cpp: C++ arcus terminal class to be wrapped into python.
//

#include "stdafx.h"
#include "arcus.h"


#define PERFORMAX_RETURN_SERIAL_NUMBER		0

using namespace std;

//const char *Arcus::CleanBuffer = "                                                               ";

Arcus::Arcus() 
{

}

int Arcus::Connect() 
{
	/* be sure that is not arcus connected*/
	fnPerformaxComClose(this->m_hUSBDevice);
	
	/* Get count of arcus devices in usb bus */
	dwNumDevices = this->GetNumDevices();

	/* Check if any device is available */
	if (!fnPerformaxComGetNumDevices(&this->m_dwNumDevices))		{
		//error message
		cout << "No arcus devices" << endl;
		return 0;
	}

	/* get product strig */
	fnPerformaxComGetProductString(0, this->ProductString, PERFORMAX_RETURN_SERIAL_NUMBER);

	/* define timeouts */
	if (fnPerformaxComSetTimeouts(10000, 10000))
	{
		/*Open connection to arcus device*/
		if (fnPerformaxComOpen(0, &this->m_hUSBDevice))
		{
			cout << "Arcus device connected" << endl;
			//fnPerformaxComFlush(&this->m_hUSBDevice);
			return 1;
		} else {
			cout << "Cannot connect Arcus device" << endl;
			return 0;
		}
	}
	return 0;
}

Arcus::~Arcus(){
	//this->Close();
	//delete	m_hUSBDevice;
};

void Arcus::SendAndRecive(char *input_buf, char *output_buf)
{
	/* copy input buffer to command buffer */
	strcpy_s(this->CmdBuffer, input_buf);

	/* Send command to arcus device and recive response */
	fnPerformaxComSendRecv(this->m_hUSBDevice, this->CmdBuffer, 64, 64, this->ResponseBuffer);
	
	/* Copy response to output buffer */
	for(int i=0; i<64; i++){
		*(output_buf + i) = this->ResponseBuffer[i];
	}

}

void Arcus::Close()
{
		/* Close connection */
		fnPerformaxComClose(this->m_hUSBDevice);
}

int main (char *input_buf, char *output_buf){
	Arcus *app = new Arcus();
	app->Connect();
}
