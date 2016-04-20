author: ObliVion
date: 2015-12-03 16:02
tags: esp8266, esp201, Microcontroller, JTAG, debug,OpenOCD
title: ESP8266 (esp201) debugging with JTAG on OpenOCD.
type: post
template: post
status: hidden

I have been seeing stories of being able to debug the ESP8266 using either
JTAG or serial. The serial option is acting up, and I have only
recently gotten an ALTERA USB Blaster clone (a JTAG to USB interface).


Pin numbers on the esp201 (counter clockwise like etc. DIP8)

 | Pin nr. | Name |
 |:-------:|:-----| 
 | 1 | GPIO0 |
 | 2 | GPIO2 |
 | 3 | D2 |
 | 4 | CLK |
 | 5 | CMD |
 | 6 | D0 |
 | 7 | D1 |
 | 8 | D3 |
 | 9 | GPIO4 |
 | 10 | 3.3V |
 | 11 | 3.3V |
 | 12 | GND |
 | 13 | GND |
 | 14 | GPIO5 |
 | 15 | T_OUT |
 | 16 | RST |
 | 17 | CHIP_ENABLE |
 | 18 | XPD |
 | 19 | GPIO14 |
 | 20 | GPIO12 |
 | 21 | GPIO13 |
 | 22 | GPIO15 |

#USB Blaster JTAG to ESP8266 (esp201) connection.#

 | JTAG Signal | ESP8266 Pin | JTAG Pin (20 pins) | (USB Blaster JTAG Pin (10 pins) |
 |-------------|:----------------:|:------------------:|:-------------------:|
 | TMS | GPIO14 | 7 | 5 |
 | TDI | GPIO12 | 5 | 9 |
 | TCK | GPIO13 | 9 | 1 |
 | TDO | GPIO15 | 13 | 3 |
 | RST | RST | 15 | 8 |
 | GND | GND | 2, 4, 6, 8, 10, 12, 14, 16, 18, and 20 | 2 and 10 |
 
##USB Blaster.##
 
 | Name	| Pin | Description |
 |---|---|---|
 | TCK | 1 | Clock signal.|
 | GND | 2 | Ground. |
 | TDO | 3 | Data from device. |
 | VTG | 4 | Target power supplied by the device board. | 
 | TMS | 5 | JTAG state machine control. |
 | nSRST | 6 | Reset (optional). Used to reset the target device. |
 | nTRST | 8 | Test reset (optional). |
 | TDI | 9 | Data to device. |
 | GND | 10 | Ground. |
 
###10 pin female IDC plug.###
 
		 ___
	-----   -----
	| 1 3 5 7 9 |
	| 2 4 6 8 10|
	-------------

###10 pin male IDC plug on USB Blaster.###
 
	-----   -----
	| 9 7 5 3 1 |
	|10 8 6 4 2 |
	-------------

#OpenOCD.#

Install libftd2xx

USB ID 09fb:6001

https://github.com/sysprogs/esp8266-openocd

./configure --enable-usb_blaster_libftdi --enable-usb-blaster-2 --enable-usb_blaster_ftd2xx

##Take 2.##

Modifications done by sysprogs are targeting Windows and seems to break
stuff on Linux. We do a little dancing and chanting to make this right.

###Install libusb-1.x.####

####Debian:####

	apt install libusb-1.0-0-dev libftdi-dev

###Configure.###

Make scripts used to configure esp8266-openocd executable by user.

	chmod u+x configure jimtcl/configure jimtcl/autosetup/find-tclsh
	
Rebuild automake build system to avoid missing `aclocal-1.13.sh`:

	ln -sf readme.md README
	autoreconf -vfi
	
Configure esp8266-openocd, remember to enable the JTAG device drivers that you need (usb-blaster, usb-blaster II, Raspberry Pi, in this case):

	./configure --enable-doxygen-pdf --prefix=/usr/local  --enable-verbose --enable-usb-blaster-2 --enable-usb_blaster_libftdi --enable-bcm2835gpio

###Build.###

Make scripts used to build esp8266-openocd executable by user.

	chmod u+x src/helper/bin2char.sh
	
Remove the line (281) `#define HAVE_LIBUSB_ERROR_NAME` from ` src/helper/replacements.h` and build.

Replace `COMMAND_HELPER` with 
	
	make
	
###Install.###

	make install


