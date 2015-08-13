gcc -Wall -fPIC -c shutter_interface.c
gcc -shared -Wl,-soname,libshutter.so.1 -o shutter_interface.so shutter_interface.o evgpio.c -mcpu=arm9
