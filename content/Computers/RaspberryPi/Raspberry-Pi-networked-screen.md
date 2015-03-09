author: ObliVion
date: 2015-03-07 17:36
tags: Raspberry Pi, Raspbian, network, screen, synergy, ssh tunnel
title: Raspberry Pi as a networked screen (Poor mans version).
type: post
template: post
status: hidden


I needed a second screen for my netbook, as the screen real estate was not
large enough for working with QT creator comfortably. I did not want
(and did not have) a 5 meter VGA cable crossing the living room, but I
wanted to use my TV as the second monitor.

I grabbed my Raspberry Pi B, a 2GB SD-card i had in the spares, and set
out to configure the Raspberry Pi to mirror the screen on the TV from
the network.

I tried using a protocol of X, called XDMX, that is designed to do what
I wanted. I used much time, and had inconsistent results. I am sure that
 the problems where all of the [wetware](http://en.wikipedia.org/wiki/Wetware_%28brain%29)
kind, but the documentation seems really sparse, and that does not help.

The solution for now, is less elegant. I installed a basic LXDE
environment on the Raspberry Pi. Shared the keyboard and mouse using 
[Synergy](http://synergy-project.org/), and run the X applications
on the netbook, through a ssh tunnel from the Raspberry Pi.


First things first, an OS (Raspberry Pi).
=========================================

The standard Raspbian image will not fit on the 2GB card I had, but
[The minimal Raspbian unattended netinstaller](https://github.com/debian-pi/raspbian-ua-netinst)
comes to the rescue.

Simply download the installer image, write it to the SD-card, and boot
the Pi, with it. Instructions for doing this can be found in the 
[README](https://github.com/debian-pi/raspbian-ua-netinst/blob/master/README.md).
ua-netinst will start installing a Raspbian system, from the Internet, 
this takes a while.

I then lost my whits and asked the Pi to install a full lxde environment,
it took ages! After starting from scratch, I added myself as a user, and
installed X and a minimal LXDE environment.
	
	adduser username
	
	apt-get install keyboard-configuration	
	apt-get install xserver-xorg
	apt-get install lxde-core
	apt-get install xinit

and Synergy

	apt-get install synergy


Synergy (control node).
=======================

Synergy acting as a server, needs a configuration file in `/etc/synergy.conf`
to setup the layout.

I have the Raspberry Pi (connected to the TV) with the host name `pi`, 
and the netbook called `ace2` (the alias section). The TV is left of the
netbook.
  	
	section: screens
			pi:
			netbook:
	end

	section: links
			pi:
					left = netbook
			netbook:
					right = pi
	end

	section: aliases
		netbook:
			ace2
	end

Start the Synergy server.

	synergys
	

Final step (Raspberry Pi).
==========================

I needed to run QT creator on the TV, but you can run any X application.
Complex things like video and fancy GUIS, are slow. Probably due to
missing hardware acceleration and network speed.

I start the Synergy client, after which the netbook mouse and keyboard
works on the Pi as well.

	synergy (IP address of the controlling computer)
	
Then I ssh into the the netbook with X tunneling and compression, and
start the program that I want to use. I now have the program (qtcreator)
running on the TV, but can use the netbook keyboard and mouse to control 
it.

	ssh -CX (IP address of the controlling computer)
	qtcreator

