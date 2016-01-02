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
