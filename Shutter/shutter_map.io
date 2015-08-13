This is intended as a reference to the dio assignment using the TS7250V2 PC104.

See schematic reference for more information.

All ISA ports are specified as Digital Input

DIO ports are used as output (but can be configured as both).

ISA port 61 needs to be set as either high (output) or low (input) to specify ISA bus IO direction.

	PC104 Assignment	EVGPIO Assignment

Hall 1:
	ISA_DAT_00	25
	ISA_DAT_01	26
	ISA_DAT_02	27
	ISA_DAT_03	28

Hall 2:	
	ISA_DAT_04	29
	ISA_DAT_05	30
	ISA_DAT_06	31
	ISA_DAT_07	32

TTL From Leach:
	ISA_DAT_08	33

Spare:
	ISA_DAT_09	34
	ISA_DAT_10	35

Valve:
	DIO_01		76
	DIO_03		77
