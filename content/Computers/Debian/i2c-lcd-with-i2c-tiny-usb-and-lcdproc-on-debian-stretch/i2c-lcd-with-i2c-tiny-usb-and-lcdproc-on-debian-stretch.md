author: ObliVion
date: 2018-03-03 21:04
tags: I2C, digispark, lcdproc, LCD, Debian, I2C-Tiny-USB, HD44780
title: I2C LCD with I2C tiny USB and lcdproc on Debian stretch
template: post

These instructions will enable lcdproc to display computer status on Debian stretch using a [Digispark microcontroller board](http://digistump.com/wiki/digispark), an [I2c to HD44780 interface](https://tronixlabs.com.au/news/tutorial-serial-i2c-backpack-for-hd44780compatible-lcd-modules-with-arduino/), and a 20x4 HD44780 chracter LCD.

!{test}($LOCALURL/connected.png)

The Digispark microcontroller connected to the HD44780 LCD via the I2C to HD44780 interface, a spare interface is shown at the top left

Lcdproc support the HD44780 interface conneted via I2C but uses a pin mapping that is different from the above board. However, an [updated driver](https://github.com/wilberforce/lcdproc) exists, allowing cutomising the pin mapping of the I2C to HD44780 interface. To use this driver the Debian package has to be rebuild substituting the driver sources.

# Preperations

## Digispark

Information on installing the I2C-tiny-USB firmware can be found here: [https://github.com/harbaum/I2C-Tiny-USB/tree/master/digispark](https://github.com/harbaum/I2C-Tiny-USB/tree/master/digispark)

## Debian Machine

Install the required dependencies to build the debian package:

    apt install build-essential autotools-dev cme debhelper dh-systemd libg15-dev libg15daemon-client-dev libg15render-dev liblircclient-dev libncurses5-dev libusb-1.0-0-dev libxosd-dev pkg-config libftdi-dev libusb-dev i2c-tools

Download and unpack the Debian package source:

    wget http://http.debian.net/debian/pool/main/l/lcdproc/lcdproc_0.5.7.orig.tar.gz
    wget http://http.debian.net/debian/pool/main/l/lcdproc/lcdproc_0.5.7-7.debian.tar.xz

    tar xvzf lcdproc_0.5.7.orig.tar.gz lcdproc-0.5.7/
    cd lcdproc-0.5.7/
    tar xvJf ../lcdproc_0.5.7-7.debian.tar.xz 
    cd ..

Clone the modified I2C HD44780 driver:

    git clone https://github.com/wilberforce/lcdproc

Copy the modified driver source into the Debian sources:

    cd lcdproc
    cp -rv docs server ../lcdproc-0.5.7/.
    cd ..

# Building the package

    cd lcdproc-0.5.7
    dpkg-buildpackage -b

# Installing the package

    cd ..
    dpkg -i lcdproc_0.5.7-7_i386.deb

# Finding the I2C LCD

First load the needed I2C kernel moduled:
    modprobe i2c-dev
    modprobe i2c-tiny-dev

Next find the I2C device that the LCD is attached to, use i2cdetect -l to list all I2C devices in the system:

    $$ i2cdetect -l
    i2c-1   i2c             i2c-tiny-usb at bus 001 device 004      I2C adapter
    i2c-0   smbus           SMBus Via Pro adapter at 5000           SMBus adapter

The adapter we are looking for is the `i2c-tiny-usb` with bus number `001` and available at device node `/dev/i2c-1`.

The address of the LCD is also found using i2cdetect. This time called with the `-y` parameter followed by the bus number found above. 

    $$ i2cdetect -y 1
        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
    00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
    10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    20: -- -- -- -- -- -- -- 27 -- -- -- -- -- -- -- -- 
    30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
    70: -- -- -- -- -- -- -- --

From the above output the address is the default of `0x27`.

# Configure

Add the following lines to `/etc/modules` to load the needed I2C modules at boot:

    i2c
    i2c-tiny-usb

Edit `/etc/LCDd.conf` to look like below. Adjust `Device, and `Port` with the values learned above.

    [server]
    DriverPath=/usr/lib/i386-linux-gnu/lcdproc/
    Driver=hd44780
    NextScreenKey=Right
    PrevScreenKey=Left
    ReportToSyslog=yes
    ReportLevel=2
    ToggleRotateKey=Enter
    WaitTime=3
    ServerScreen=no


    [menu]
    DownKey=Down
    EnterKey=Enter
    MenuKey=Escape
    UpKey=Up

    [hd44780]
    ConnectionType=i2c
    Device=/dev/i2c-1
    OutputPort=no
    Port=0x27
    Backlight=no
    Size=20x4
    DelayBus=false
    DelayMult=1
    Keypad=no
    # edit the pin configurations for your i2c module (Note2)
    i2c_line_RS=0x01
    i2c_line_RW=0x02
    i2c_line_EN=0x04
    i2c_line_BL=0x08
    i2c_line_D4=0x10
    i2c_line_D5=0x20
    i2c_line_D6=0x40
    i2c_line_D7=0x80

My `/etc/lcdproc.conf` contains the following:
 
    # LCDproc client configuration file

    ## general options ##
    [lcdproc]
    # address of the LCDd server to connect to
    Server=localhost

    # Port of the server to connect to
    Port=13666

    # set reporting level
    ReportLevel=2

    # report to to syslog ?
    ReportToSyslog=false

    # run in foreground [default: false; legal: true, false]
    #Foreground=true

    # PidFile location when running as daemon [default: /var/run/lcdproc.pid]
    #PidFile=/var/run/lcdproc.pid

    # slow down initial announcement of modes (in 1/100s)
    #delay=2

    # display name for the main menu [default: LCDproc HOST]
    #DisplayName=lcdproc


    ## screen specific configuration options ##

    [CPU]
    # Show screen
    Active=True
    OnTime=1
    OffTime=2
    ShowInvisible=false


    [Iface]
    # Show screen
    Active=True

    # Show stats for Interface0
    Interface0=eth0
    # Interface alias name to display [default: <interface name>]
    Alias0=LAN

    # Show stats for Interface1
    Interface1=eth1
    Alias1=WAN

    # Show stats for Interface2
    Interface2=tun0
    Alias2=VPN

    # for more than 3 interfaces change MAX_INTERFACES in iface.h and rebuild

    # Units to display [default: byte; legal: byte, bit, packet]
    unit=byte

    # add screen with transferred traffic
    transfer=TRUE


    [Memory]
    # Show screen
    Active=True


    [Load]
    # Show screen
    Active=True
    # Min Load Avg at which the backlight will be turned off [default: 0.05]
    LowLoad=0.05
    # Max Load Avg at which the backlight will start blinking [default: 1.3]
    HighLoad=1.3


    [TimeDate]
    # Show screen
    Active=True
    # time format [default: %H:%M:%S; legal: see strftime(3)]
    TimeFormat="%H:%M:%S"
    # date format [default: %x; legal: see strftime(3)]
    DateFormat="%x"


    [About]
    # Show screen
    Active=false


    [SMP-CPU]
    # Show screen
    Active=false


    [OldTime]
    # Show screen
    Active=false
    # time format [default: %H:%M:%S; legal: see strftime(3)]
    TimeFormat="%H:%M:%S"
    # date format [default: %x; legal: see strftime(3)]
    DateFormat="%x"
    # Display the title bar in two-line mode. Note that with four lines or more
    # the title is always shown. [default: true; legal: true, false]
    #ShowTitle=false


    [BigClock]
    # Show screen
    Active=False


    [Uptime]
    # Show screen
    Active=True


    [Battery]
    # Show screen
    Active=false


    [CPUGraph]
    # Show screen
    Active=True


    [ProcSize]
    # Show screen
    Active=false


    [Disk]
    # Show screen
    Active=True


    [MiniClock]
    # Show screen
    Active=False
    # time format [default: %H:%M; legal: see strftime(3)]
    TimeFormat="%H:%M"


    # EOF

# Testing

By issuing the following command the server and the lcdproc client is started in the foreground running untill you press CTRL+C. The LCD should start displaying the screens configured in `/etc/lcdproc.conf`.

    service LCDd start
    lcdproc -f

# Making it survive reboots

Enabe LCDd at boot:

    systemctl enable LCDd

Edit `/etc/rc.local` and add `/usr/bin/lcdproc` towards the end before the line `exit 0` to have the lcdproc client start at boot.



