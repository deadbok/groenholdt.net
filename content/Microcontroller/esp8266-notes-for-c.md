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
 - The IoT SDK is single tasked and event driven. I've always found event
   driven programming a pain, but this implementation stinks. There is no way
   to return to the system, in the middle of processing, to not stall the
   system tasks. The docs, says that you not may stay in a function for more 
   than 10 ms, without the system code getting behind. If I were to start
   over I would try the FreeRTOS SDK, unfortunately it seems that Espressif is
   giving it less love.

Network.
--------
 - Some basic code for connecting to a WIFI. [GitHub](https://github.com/deadbok/esp8266-connect-ap)
 - The connect callback returns a pointer to the `struct espconn` in the `arg` 
   parameter. It is not the same as the one used by `espconn_accept`.
 - The `disconnect_callback`receives a pointer to the listening connection,
   *not* the active connected one, at least when in TCP server mode.
 - In `struct espconn`, member reverse, seems to be free to use., except in the
   disconnect callback, where it suddenly has a new value.
   
Flash.
------
 - It seems the file system of choice is best placed after the code in flash.
 - On suggestion from [Dave Hylands](http://www.davehylands.com/), I use a ZIP
   file as file system image. The file is uncompressed and used as a simple
   container.

