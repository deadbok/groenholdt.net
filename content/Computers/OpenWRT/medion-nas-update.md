author: ObliVion
date: 2015-02-21 19:23
slug: OpenWRT-update-medion-OX820-based-NAS
tags: OpenWRT, NAS, Medion MD86517, update
title: Installing an updated OpenWRT image 
type: post
template: post


Installing an updated OpenWRT image.
====================================

*[OpenWrt Sysupgrade](http://wiki.openwrt.org/doc/howto/generic.sysupgrade)*

OpenWRT has a command, `sysupgrade`, that is used to upgrade the flash 
image from an update file. I have not been able to get this to work, and
have ended up installing LUCI, the web configuration interface, 
every time I need to update the root file system.

	opkg install luci
	
This opens another can of worms, since lighttpd is happily serving pages
on port 80, where LUCIs web server, [uHTTPd](http://wiki.openwrt.org/doc/howto/http.uhttpd),
wants to be. To get around this, I told uHTTPd to use some other ports.
To do this, change the ports in the lines containing `listen` in
`/etc/config/uhttpd`, like so:

	config uhttpd 'main'
		list listen_http '0.0.0.0:8080'
		list listen_http '[::]:8080'
		list listen_https '0.0.0.0:4430'
		list listen_https '[::]:4430'

Then restart uHTTPd:

	/etc/init.d/uhttpd restart

LUCI will now be available on the current IP address, on port 8080 and
encrypted on 4430. Use the root user/password to login in, and use
`openwrt-oxnas-stg212-ubifs-sysupgrade.tar` to update the device.

After flashing the firmware, all packages need to be reinstalled. Opkg
will probably complain about changed config files, but this just means
our configuration changes have been kept.

