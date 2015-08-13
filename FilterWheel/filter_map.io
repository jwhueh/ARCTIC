This is intended as a reference to the dio assignment using the TS7250V2 PC104.

See schematic reference for more information.

All ISA ports are specified as Digital Input

DIO ports are used as output (but can be configured as both).

ISA port 61 needs to be set as either high (output) or low (input) to specify ISA bus IO direction.

to test evgpio use command ./evgpioctl -w

	PC104 Assignment	EVGPIO Assignment

FilterWheel Hall:
	ISA_DAT_11	36
	ISA_DAT_12	37
	ISA_DAT_13	38
	ISA_DAT_14	39
	ISA_DAT_15      40

Detent Switches:	
	DIO_11		81
	DIO_13		82

Solenoid:
	DIO_15		83
