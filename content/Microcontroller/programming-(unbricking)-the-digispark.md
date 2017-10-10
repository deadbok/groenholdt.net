author: ObliVion
date: 2017-10-10 08:03
slug: programming-(unbricking)-the-digispark
tags: arduino, avr, digispark, raspberry pi
title: Programming (unbricking) the DigiSpark using a Raspberry Pi
type: post
template: post


If your DigiSpark is no longer getting programmed from the Arduino IDE, when
plugging it in, you might have to re-program the [Micronucleus bootloader][4b92b992]. You can do this using the Raspberry Pi if you do not have an AVR programmer.

# Preperation

Install the AVRDUDE programmer on the Raspberry Pi:

    apt-get install avrdude

Copy the default AVRDUDE configuration file to your home directory.

    cp /etc/avrdude.conf ~/avrdude_gpio.conf
    nano ~/avrdude_gpio.conf

Add this to the end of the file to make AVRDUDE use the Raspberry
Pi GPIO port as programming port.

    # Raspberry PI GPIO configuration for avrdude.
    # Change the lines below to the GPIO pins connected to the AVR.
    programmer
      id    = "rpi";
      desc  = "Use the Linux sysfs interface to bitbang GPIO lines";
      type  = "linuxgpio";
      reset = 12;
      sck   = 24;
      mosi  = 23;
      miso  = 18;
    ;

Next, download the [Micronucleus bootloader][4b92b992] file called `micronucleus-1.06.hex`.

    wget https://github.com/micronucleus/micronucleus/raw/80419704f68bf0783c5de63a6a4b9d89b45235c7/firmware/releases/micronucleus-1.06.hex

Connect the DigiSpark to the Raspberry Pi using the table below.

|AVR pin name | DigiSpark pin name | RPI pin name | RPI pin number |  
|:-----------:|:------------------:|:------------:|:--------------:|
|    ICSP VCC |                 5V |           5V |              2 |
|    ICSP GND |                GND |   Ground/GND |              6 |
|  ICSP RESET |                 P5 |     GPIO #12 |             32 |
|    ICSP SCK |                 P2 |     GPIO #24 |             18 |
|   ICSP MOSI |                 P0 |     GPIO #23 |             16 |
|   ICSP MISO |                 P1 |     GPIO #18 |             12 |

When the DigiSpark is connected run this command from your home directory to program the AVR with the bootloader.

    sudo avrdude -p attiny85 -C avrdude_gpio.conf -c rpi -U flash:w:micronucleus-1.06.hex:i -U lfuse:w:0xF1:m -U hfuse:w:0x5F:m

AVRDUDE should respond something like this:

    avrdude: AVR device initialized and ready to accept instructions

    Reading | ################################################## | 100% 0.00s

    avrdude: Device signature = 0x1e930b
    avrdude: NOTE: "flash" memory has been specified, an erase cycle will be performed
             To disable this feature, specify the -D option.
    avrdude: erasing chip
    avrdude: reading input file "micronucleus-1.06.hex"
    avrdude: writing flash (8162 bytes):

    Writing | ################################################## | 100% 1.28s

    avrdude: 8162 bytes of flash written
    avrdude: verifying flash memory against micronucleus-1.06.hex:
    avrdude: load data flash data from input file micronucleus-1.06.hex:
    avrdude: input file micronucleus-1.06.hex contains 8162 bytes
    avrdude: reading on-chip flash data:

    Reading | ################################################## | 100% 1.09s

    avrdude: verifying ...
    avrdude: 8162 bytes of flash verified
    avrdude: reading input file "0xF1"
    avrdude: writing lfuse (1 bytes):

    Writing | ################################################## | 100% 0.00s

    avrdude: 1 bytes of lfuse written
    avrdude: verifying lfuse memory against 0xF1:
    avrdude: load data lfuse data from input file 0xF1:
    avrdude: input file 0xF1 contains 1 bytes
    avrdude: reading on-chip lfuse data:

    Reading | ################################################## | 100% 0.00s

    avrdude: verifying ...
    avrdude: 1 bytes of lfuse verified
    avrdude: reading input file "0x5F"
    avrdude: writing hfuse (1 bytes):

    Writing | ################################################## | 100% 0.01s

    avrdude: 1 bytes of hfuse written
    avrdude: verifying hfuse memory against 0x5F:
    avrdude: load data hfuse data from input file 0x5F:
    avrdude: input file 0x5F contains 1 bytes
    avrdude: reading on-chip hfuse data:

    Reading | ################################################## | 100% 0.00s

    avrdude: verifying ...
    avrdude: 1 bytes of hfuse verified

    avrdude: safemode: Fuses OK (E:FE, H:5F, L:F1)

    avrdude done.  Thank you.

After which the Arduino IDE should be able to program it again.


[4b92b992]: https://github.com/micronucleus/micronucleus "Micronucleus bootloader"
