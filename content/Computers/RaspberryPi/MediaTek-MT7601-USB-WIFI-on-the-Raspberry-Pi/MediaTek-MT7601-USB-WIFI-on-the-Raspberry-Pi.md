author: ObliVion
date: 2014-05-21 20:00
tags: MT7601, WIFI, Raspberry Pi, Raspbian
title: MediaTek MT7601 USB WIFI on the Raspberry Pi
type: post
template: post


I bought an USB WIFI dongle, on ebay, to use with the Raspberry Pi. I thought
the chip was a Ralink chip which is supported, but it turned out it was a 
MediaTek MT7601.

	Bus 001 Device 005: ID 148f:7601 Ralink Technology, Corp.
	
The driver is available at their web side download page [here](http://www.mediatek.com/en/downloads/).
Find the one called "MT7601U USB". I have the file mirrored [here]($LOCALURL/DPO_MT7601U_LinuxSTA_3.0.0.4_20130913.tar.bz2).

I found [these](http://va3paw.com/2014/03/16/hsmm-mesh-on-raspberry-pi/#more-629)
instructions to work for building the driver. All this is for Raspian and I will
elaborate a bit.

Driver
======

Become root.

	sudo -s

Download latest updates.

	apt-get update
 	apt-get upgrade
 	rpi-update

Download linux kernel source, this is needed to compile the driver module.
 
	cd /usr/src
 	git clone https://github.com/raspberrypi/linux.git
 	sudo ln -s /usr/src/linux /lib/modules/`uname -r`/build
 	cd linux

Compile the kernel with the current kernel config from the running system.

	make mrproper
	zcat /proc/config.gz > .config
	cp .config .config.org
 	make modules_prepare
 
Download the module symbols of the current kernel, to avoid having to 
recompile the kernel.
 
 	wget https://raw.github.com/raspberrypi/firmware/master/extra/Module.symvers

Get the MT7601 USB driver into your home directory. Then, lets uncompress the file. 

	cd ~ 
	tar -xvjpf DPO_MT7601U_LinuxSTA_3.0.0.4_20130913.tar.bz2 
	cd DPO*

The default driver is really noisy and spits out a lot of debug information. This
behaviour can be stopped by changing a line in ``os/linux/rt_linux.c`` from:

	ULONG RTDebugLevel = RT_DEBUG_TRACE;

to:

	ULONG RTDebugLevel = 0; // RT_DEBUG_TRACE; 

Finally build the driver and install it.

	sudo make
	sudo make install
	
Raspbian configuration
======================

Configure the ra0 interface for DHCP and make it start at boot. Edit ``/etc/network/interfaces``
to look like:

	auto lo

	iface lo inet loopback
	iface eth0 inet dhcp

	auto ra0
	allow-hotplug ra0
	iface ra0 inet dhcp
	wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
	iface default inet dhcp

Then add your WIFI name and key to ``/etc/wpa_supplicant/wpa_supplicant.conf``.

	ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
	update_config=1

	network={
        	ssid="YOURWIFINAME"
        	key_mgmt=WPA-PSK
        	psk="YOURPASSWORD"
	}
