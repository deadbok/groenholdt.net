author: ObliVion
date: 2015-04-17 21:40
tags: esp8266, esp12, Microcontroller, c
title: ESP8266 notes for C programming.
type: post
template: post

Following up on the general notes, here I some notes on programming for
the ESP8266 in C. I use Linux for development, but most of this is OS
independent.

General.
--------
 - Prefixing a function with "ICACHE_FLASH_ATTR" places it in flash,
   not doing so places the function in RAM.

Network.
--------
 - Some basic code for connecting to a WIFI. [GitHub](https://github.com/deadbok/esp8266-connect-ap)
 - The connect callback returns a pointer to the `struct espconn` in the `arg` 
   parameter. It is not the same as the one used by `espconn_accept`.
 - In `struct espconn`, member reverse, seems to be free to use.
 - The `disconnect_callback`receives a strange pointer in `arg`. It seems to be
   a valid `struct espconn`, with the right data. The pointer itself however, 
   does not have the address, of the structure that was supplied, when the
   connection was created. Could be a copy?
