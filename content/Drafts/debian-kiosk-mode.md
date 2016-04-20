author: ObliVion
date: 2015-08-07 16:25
status: hidden
tags: debian, kiosk
title: Debian kiosk setup
template: post

Debian kiosk setup
==================

Install stuff
-------------

	apt-get install xorg lightdm matchbox-window-manager chromium rsync
	
User
----

	adduser kiosk

Session startup script
----------------------

	cp -r /home/kiosk /opt/
	cd /opt/kiosk/
	chmod -R a+r .
	touch .xsessionrc
	chmod a+x .xsessionrc
	
Add this to -xsessionrc:

	#Disable screen power saving
	xset s off
	xset -dpms
	#Start Window Manager
	matchbox-window-manager  -use_titlebar no &
	#Update files in /home/kiosk and start chromium
	while true; do
		rsync -qr --delete --exclude='.Xauthority' /opt/kiosk/ $$HOME/
		chromium --app=http://straylight:5000
	done

LightDM autologin
-----------------

Edit ```/etc/lightdm/lightdm.conf``` and change to following;

	autologin-user = kiosk
	autologin-timeout = 0
