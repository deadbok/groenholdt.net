author: ObliVion
date: 2015-04-17 21:31
tags: esp8266, esp12, Microcontroller
title: ESP8266 notes.
type: post
template: post

The buggers have been lying around while life happened, and I was waiting
for the last one I ordered, which was on a neat breakout board. Well I
got tired of waiting, and started playing with the ESP12 version. These
are some random notes, of things I have discovered during my
experiments.

 - My ESP12's have their GPIO4 & GPIO5 pins swapped on the silkscreen.
 - The toolchain for the [Arduino ESP8266 IDE](https://github.com/esp8266/Arduino) seems to be 64-bit.
 - I cannot reliably program using a PL2303 adaptor, but my Raspberry Pi
   Model B's serial port works fine.
 - In SoftAP mode, the SDK seems to set up a DHCP server on 192.168.4.1, all
   without me doing anything but setting the mode, and the AP config.
 - Baud rate at boot is 74880.
 - Untested [Zero-wire auto-reset](http://nerdralph.blogspot.dk/2015/04/zero-wire-auto-reset-for-esp8266arduino.html).
   (`esptool.py` needs a modification to send the break signal).
