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

1 GPIO0
2 GPIO2
3 D2
4 CLK
5 CMD
6 D0
7 D1
8 D3
9 GPIO4
10 3.3V
11 3.3V
12 GND
13 GND
14 GPIO5
15 T_OUT
16 RST
17 CHIP_ENABLE
18 XPD
19 GPIO14
20 GPIO12
21 GPIO13
22 GPIO15

OpenOCD.
========

Install libftd2xx

USB ID 09fb:6001

https://github.com/sysprogs/esp8266-openocd

./configure --enable-usb_blaster_libftdi --enable-usb-blaster-2 --enable-usb_blaster_ftd2xx

Take 2.
-------

Modifications done by sysprogs are targeting Windows and seems to break
stuff on Linux. We do a little dancing and chanting to make this right.

###Install libusb-1.x.####

####Debian:####

	apt install libusb-1.0-0-dev libftdi-dev

###Configure.###

Make scripts used to configure esp8266-openocd executable by user.

	chmod u+x configure jimtcl/configure jimtcl/autosetup/find-tclsh
	
Rebuild automake build system to avoid missing `aclocal-1.13.sh`:

	touch README
	autoreconf -vfi
	
Configure esp8266-openocd, remember to enable the JTAG device drivers that you need (usb-blaster, usb-blaster II, Raspberry Pi, in this case):

	./configure --enable-doxygen-pdf --prefix=/usr/local  --enable-verbose --enable-usb-blaster-2 --enable-usb_blaster_libftdi --enable-bcm2835gpio

###Build.###

Make scripts used to build esp8266-openocd executable by user.

	chmod u+x src/helper/bin2char.sh
	
Remove the line (281) `#define HAVE_LIBUSB_ERROR_NAME` from ` src/helper/replacements.h` and build.
	
	make
