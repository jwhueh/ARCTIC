Python terminal driver for Arcus devices 
Compatible with Python 2.7. 32-bit


---------------
1 PACKAGE CONTENTS---------------

--
           

This driver uses swig to wrap PerformaxCom.lib.

This package includes source codes and binaries. 




---------------
2 RELEASE NOTES
---------------

-----
 
1.0 (Rel. April 2013)-- 
    
* Python terminal driver based on PerformaxCom.lib and swig(ArcusDevice)
    
* higher level classes created (ArcusStepperChannel, ArcusLinearAxis) for easy use of wrapper   





---------------
3 INSTALL BINARIES 



---------------

-----
--Windows
   
Copy _Arcus.pyd, Arcus.py and ArcusDevice.py into your project directory or include in PYTHONPATH 



---------------
4 BUILD AND INSTALL FROM SOURCE 



---------------

-----

Files:

Arcus.cpp, Arcus.h  C++ interface to PerformaxCom.dll


Arcus.i SWIG interface file to generate python wrappers to C++
 Arcus.py, 

Arcus_wrap.cxx SWIG generated interface classes


ArcusDevice.py python module to be used by user. 

Contains basic class for terminal communication with arcus device and some higher classes to easily use arcus device(see documentation inside)

--

Windows

   
Install python(tested on python 2.7.2) and setup enviroment variables $(PYTHON_INCLUDE) and $(PYTHON_LIB).

   
From \src\Arcus\PerformaxCom copy 32 bit version of PerformaxCom.lib to \src\Arcus\ directory
   

Select release configuration and platform(32 bit).
   

Build
   
Copy PerformaxCom.dll, SiUSBXp.dll, ArcusDevice.py from binaries directory and Arcus.py and _Arcus.pyd from build directory to target directory
   

Run ArcusDevice.py

---------------
5 Example 



---------------

-----

5 USE 

After installation see the examples in the bottom of ArcusDevice.py file


NOTE: Install PerformaxCom and SiUSBXp (32 bit)
Bin --> Open ArcusDevice.py in Python IDE --> Run --> Terminal Commands

For Windows:
Download Swig for Windows: http://www.swig.org/download.html
Copy Arcus.i into Swig Folder
Navigate to folder using terminal/command prompt
Type in "swig -python -c++ Arcus.i"
This generates two files: Arcus.py and Arcus_wrap.cpp

// But where does _Arcus.pyd come from?
// _Arcus.pyd is its own DLL.