#include <windows.h>
#include <stdlib.h>
#include <iostream>

extern "C" __declspec(dllimport) BOOL _stdcall fnPerformaxComGetNumDevices(OUT LPDWORD lpNumDevices);
extern "C" __declspec(dllimport) BOOL _stdcall fnPerformaxComGetProductString(IN DWORD dwNumDevices, OUT LPVOID lpDeviceString, IN DWORD dwOptions);	
extern "C" __declspec(dllimport) BOOL _stdcall fnPerformaxComOpen(IN DWORD dwDeviceNum, OUT HANDLE* pHandle);
extern "C" __declspec(dllimport) BOOL _stdcall fnPerformaxComSendRecv(IN HANDLE pHandle, 
													IN LPVOID wBuffer, 
													IN DWORD dwNumBytesToWrite,
													IN DWORD dwNumBytesToRead,
													OUT LPVOID rBuffer);
extern "C" __declspec(dllimport) BOOL _stdcall fnPerformaxComWrite(IN HANDLE pHandle, LPVOID Buffer, DWORD dwNumBytesToWrite, OUT LPDWORD lpNumBytesWritten);
extern "C" __declspec(dllimport) BOOL _stdcall fnPerformaxComRead(IN HANDLE pHandle, LPVOID Buffer, DWORD dwNumBytesToRead, OUT LPDWORD lpNumBytesReturn);
extern "C" __declspec(dllimport) BOOL _stdcall fnPerformaxComClose(IN HANDLE pHandle);
extern "C" __declspec(dllimport) BOOL _stdcall fnPerformaxComSetTimeouts(IN DWORD dwReadTimeout, DWORD dwWriteTimeout);
//extern "C" __declspec(dllimport) BOOL _stdcall fnPerformaxComFlush(IN HANDLE pHandle);

///////////////////////////////////////////////////////////////////////////////////////////////////////////////Dlg

#if _MSC_VER > 1000
#pragma once
#endif

//header file for C++ arcus terminal class to be wrapped into python
class Arcus
{
	public:
		Arcus();//constructor
		~Arcus();//descructor
		int Connect();//Connect to arcus device
		DWORD GetNumDevices(){return m_dwNumDevices;}//get number of arcus devices

		void SendAndRecive(char *input_buf, char *output_buf);//Send and recieve terminal commands

		void Close();//close connection to arcus device
		
//		DWORD m_dwNumDevices;

//		public:
//			virtual BOOL InitInstance();

	protected:
		HANDLE	m_hUSBDevice;
		BOOL	m_bIsConnected;
		DWORD   m_dwNumDevices;
		DWORD	dwNumDevices, i;
		char	ProductString[128];
		char	CmdBuffer[64], ResponseBuffer[64];
		//static const char *CleanBuffer;

};