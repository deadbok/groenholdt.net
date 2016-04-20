author: ObliVion
date: 2016-04-20 22:20
tags: WakeLog, ESP8266, Sming, Android, Microcontroller
title: WakeLog simple WIFI enabled event logger - Introduction.
type: post
template: post
status: hidden


Lately I have had the need for a device to do some simple logging.
After some brianstorming I made this list of features:

 * Battery operated.
 * Self contained.
 * Log data readable wirelesly.
 
I came to the conclusion that the events I wanted to log, were on/off
type events, like logging whenever my doorbell is rung. Using an
ESP8266 module (ESP12), to log the events to the flash memory on the
module, seemed feasible even using battery power, since the module only
needed power when an event triggered it. To keep track of the time, when
the ESP8266 was off, a real-time clock was needed.

 * Use the ESP8266 as microcontroller, log storage and wireless 
   interface.
 * Use a DS3231 RTC module to keep the time.
 * Leave the RTC running at all times.
 * Power the ESP8266 only when an event needs to be logged.

The ESP8266 firmware performs the following tasks. [GitHub](https://github.com/deadbok/WakeLog-firmware)

 * Write a log entry whenever power is applied. The log entry is written
   to a ring buffer, ensuring that the data will not overflow. If the 
   flash memory is full, the firmware starts overwriting the oldest
   entries.
 * Try connecting to a predefined access point. When logging at some
   remote connection, simply create the access point using the phones
   WIFI hotspot feature.
	* Update the ESP8266 clock and the RTC from an NTP server.
	* Create a WebSocket server. This serves the log to the phone, and
	  enabled configuration of the predefined access point. 
	* Delete the logs from flash memory.
	
The client is Android specific, I have no I-devices (except an Ipod),
and Microsoft, well ya'know... [GitHub](https://github.com/deadbok/WakeLog)

 * Download the log from the WakeLog device.
 * Export the log (Google spreadsheet?).
 * Configure the access point used by the WakeLog hardware.

