author: ObliVion
date: 2015-04-17 21:40
tags: esp8266, esp12, Microcontroller
title: ESP8266 notes for C programming.
type: post
template: post

Following up on the general notes, here I some notes on programming for
the ESP8266 in C. I use Linux for development, but most of this is OS
independent.

 - Prefixing a function with "ICACHE_FLASH_ATTR" are placed in flash,
   not doing so places the function in RAM.


   
