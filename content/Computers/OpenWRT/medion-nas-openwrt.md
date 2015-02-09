author: ObliVion
date: 2015-02-06 17:49
slug: OpenWRT-web-server-medion-OX820-based-NAS
tags: OpenWRT, NAS, Medion MD86517, web server
title: Installing an OpenWRT based webserver on the Medion OX820 based NAS 
type: post
template: post
status: hidden

After getting Gentoo to run on the Medion NAS in these posts,

 + [Medion OX820 based NAS and Gentoo]($LOCALURL../Gentoo/medion-0x820-based-nas/medion-ox820-based-nas.html)
 + [Medion NAS native kernel compile]($LOCALURL../Gentoo/medion-nas-native-kernel-compile.html)

I learned that [OpenWRT](http://openwrt.org) had been ported to the oxnas platform. This 
appealed to me, as OpenWRT is installed on the internal flash. Honestly
the Gentoo installation I had on the HDD, was better suited as a web
server, but I just wanted to play with OpenWRT. The only real reason for 
using OpenWRT instead of Gentoo, is in the hopes that the OpenWRT folks 
will keep the kernel updated.

I still have my web page, and the files from which it is generated, on
the HDD connected to the SATA port.

I recommend having a serial connection to the NAS running at all times.


Installing OpenWRT bootstrap.
=============================

This operation can only be executed once, and **may brick your device**,
after the bootstrap **there is no way to restore the original firmware**.
Because of this I can not actually check that these steps are exactly
right, but they are what i recall.

To bootstrap the installation I used the binary image from
[Gitorious openwrt-oxnas](https://gitorious.org/openwrt-oxnas/pages/install).
[Binary image](https://gitorious.org/openwrt-oxnas/openwrt-oxnas-gitorious-wiki/archive/2e5653b2c09ed9dca988f89c68f44a61e3bdde19.tar.gz).

Configure your PCs Ethernet interface to 192.168.1.2/24 and power-up the 
NAS connected directly to the PC

Setup a HTTP server on your host serving openwrt-oxnas-*-u-boot-initramfs.itb

Setup Telnet backdoor according to the hint on mikrocontroller.net login
to the web-interface at http://192.168.1.5/ open <http://192.168.1.5/r36807,/adv,/cgi-bin/remote_help-cgi?type=backdoor>
(you may have to replace the /rXXXXX,/ with the revision number shown 
in the URL after login)
The browser will wait for the CGI script to (never) end, while it’s 
doing that telnet into 192.168.1.5

now login with user root and the password also set for the web interface 
(default is 1234)

	telnet 192.168.1.5

then run

	cd /tmp/tmpfs wget http://192.168.1.2/openwrt-oxnas-stg212-u-boot-initramfs.itb
	cat /proc/mtd \# make sure kernel is /dev/mtd4 nandwrite 
	/dev/mtd4 openwrt-oxnas-stg212-u-boot-initramfs.itb 
	fw_setenv boot_stage2 nand read 64000000 440000 90000\\; go 64000000
	fw_setenv bootcmd run boot_stage2 reboot

WAIT! The new bootloader will load the appended rescue firmware and
boot. As the NAND is not yet UBI formatted when the device was
previously used with the vendor firmware the first boot of the rescue
will take more than 100 seconds to boot!

Once OpenWrt has booted the device is available on 192.168.1.1 and
awaits you on it’s web interface to flash a new firmware. You should be 
able to flash any of the <span>\*</span>sysupgrade.img files matching 
the board, however, as the device wasn’t previously ubi formatted, the 
ubinized image is most safe and straight-forward in the upgrade script.

WAIT! The update on the not-yet-ubi-formatted flash will again take up 
to several minutes. Be patient and wait FOR A LONG TIME (the device 
should however respond to ping while flashing so you can see it’s still 
alive)

Trust my binaries
-----------------

Download this tarball for the STG-212 aka. Medion/Aldi NAS. ...or build
your own firmware. You’ll need a UN*X box with a working compiler, 
GNU make and some other common toolchain components on your host.
On Ubuntu you can just run apt-get install build-essential git and 
that’s all you need to do to fulfill the build requirements. For details
have a look at the OpenWrt Wiki’s on build prerequisites.

Download sources
----------------

First clone the openwrt.org repository and then rebase the oxnas stuff 
on-top of the current OpenWrt HEAD:

    git clone git://git.openwrt.org/openwrt.git 
    cd openwrt 
    git remote add oxnas https://git.gitorious.org/openwrt-oxnas/openwrt-oxnas.git 
    git fetch oxnas 
    git checkout oxnas/master 
    git rebase origin/master

If that fails, simply to

    git rebase --abort

and go with the current oxnas/master tree. Now download the package feeds:

    cp feeds.conf.default feeds.conf
    scripts/feeds update -a 
    scripts/feeds install -a

Build firmware

    make menuconfig

Make sure to select the initramfs image with xz compression in the
Target Images submenu to create the openwrt-oxnas-*-u-boot-initramfs.itb allowing easy installation of both, stage2-loader and rescue image on devices not yet running OpenWrt. DO NOT select any additional packages as the first build of the initramfs-system needs to be smaller than 4 MiB. You can re-run make menuconfig, disable the initramfs image in Target Images and select any amount of packages you want :) (I tried a squashfs with 100MiB size, it worked great)

Save your new configuration and run

    make

This should result in images being created in the bin/oxnas folder.
Installation on the STG-212 aka. Medion/Aldi NAS

Configure your PCs Ethernet interface to 192.168.1.2/24 and power-up the 
NAS connected directly to the PC

Setup a HTTP server on your host serving openwrt-oxnas-*-u-boot-initramfs.itb

Setup Telnet backdoor according to the hint on mikrocontroller.net login
to the web-interface at http://192.168.1.5/ open <http://192.168.1.5/r36807,/adv,/cgi-bin/remote_help-cgi?type=backdoor>
(you may have to replace the /rXXXXX,/ with the revision number shown 
in the URL after login)
The browser will wait for the CGI script to (never) end, while it’s 
doing that telnet into 192.168.1.5

now login with user root and the password also set for the web interface 
(default is 1234)

	telnet 192.168.1.5

then run

	cd /tmp/tmpfs wget http://192.168.1.2/openwrt-oxnas-stg212-u-boot-initramfs.itb
	cat /proc/mtd \# make sure kernel is /dev/mtd4 nandwrite 
	/dev/mtd4 openwrt-oxnas-stg212-u-boot-initramfs.itb 
	fw_setenv boot_stage2 nand read 64000000 440000 90000\\; go 64000000
	fw_setenv bootcmd run boot_stage2 reboot

WAIT! The new bootloader will load the appended rescue firmware and
boot. As the NAND is not yet UBI formatted when the device was
previously used with the vendor firmware the first boot of the rescue
will take more than 100 seconds to boot!

Once OpenWrt has booted the device is available on 192.168.1.1 and
awaits you on it’s web interface to flash a new firmware. You should be 
able to flash any of the <span>\*</span>sysupgrade.img files matching 
the board, however, as the device wasn’t previously ubi formatted, the 
ubinized image is most safe and straight-forward in the upgrade script.

WAIT! The update on the not-yet-ubi-formatted flash will again take up 
to several minutes. Be patient and wait FOR A LONG TIME (the device 
should however respond to ping while flashing so you cAsan see it’s still 
alive)

Final configuration
-------------------

tftp
====
*Based on [uboot-oxnas: support booting appended FIT image](https://gitorious.org/openwrt-oxnas/openwrt-oxnas/commit/bda93c9f1c3c0a2142c992c6d2d3a5e729b27ce0).*

u-boot-oxnas now supports directly booting into an 64k-aligned appended
uImage. Using this feature, single loadable images to be fed into legacy
bootloaders via tftp can be used to boot modern Linux kernels.
Example:

	dd if=openwrt-oxnas-ox820-u-boot.bin bs=64k of=openwrt-oxnas-ox820-u-boot.bin.pad conv=sync
	cat openwrt-oxnas-ox820-u-boot.bin.pad openwrt-oxnas-stg212-fit-uImage-initramfs.itb > openwrt-oxnas-stg212-fit-uImage-initramfs.boot

In legacy U-Boot:

	tftp 64000000 openwrt-oxnas-stg212-fit-uImage-initramfs.boot 
	nand erase 0x440000 0x400000 
	nand write 0x64000000 0x440000 0x400000 
	setenv bootcmd nand read 0x64000000 0x440000 0x90000\\; go 0x64000000 saveenv go 64000000

(sorry guys if you got a board with 64MiB (== 0x4000000) of RAM or less, the 64000000 address is hard-coded for now, but can be changed with some effort. Let me know if anyone is affected)

Unbricking with tftp
--------------------

 + Build OpenWRT with initramfs support compressed with xz.
 + Set up a tftp server, serving ”’openwrt-oxnas-stg212-fit-uImage-initramfs.itb”’

On the device, interrupt uboot, then:

	tftp 64000000 openwrt-oxnas-stg212-fit-uImage-initramfs.itb bootm


Compiling OpenWrt.
==================

Since, for now, oxnas support is only in OpenWRT trunk, everything needs
to be build.

Getting the sources.
--------------------

Change into the directory where you want the sources to reside and do:

    git clone git://git.openwrt.org/openwrt.git 
    cd openwrt 

Custom feeds.
-------------

*If you just want a web server, and do not need setuptools for Python 3,
or my shiny site generator, you can skip this step.*

I have made a couple of custom feeds, that addresses some specific
Python 3 needs I have for my [static site
generator](https://github.com/deadbok/ssg "Static Site Generator"). To
have these packages available add the following to ```feeds.conf```:

	src-git packages https://github.com/deadbok/packages.git
	src-git deadbok https://github.com/deadbok/deadbok-openwrt.git
	
Comment out the original package line in the file.


Filesystem layout.
==================

 + ```/``` OpenWRT on the internal flash.
 + ```/mnt/data``` Root of the connected HDD.
 + ```/mnt/data/www``` Root of the pages served by lighttpd.
 + ```/mnt/data/log``` System log files.
 
 
Adding custom packages.
=======================
*[OpenWRT wiki: OPKG Package Manager](http://wiki.openwrt.org/doc/techref/opkg)*

I have chosen to compile most of the software I use, in this 
installation, as packages that must be installed after flashing the
static image.
Some of these packages are only installed for my own personal 
convenience, and some because they are needed for my [static site
generator](https://github.com/deadbok/ssg "Static Site Generator").


Serving packages for OpenWRT.
-----------------------------

Like when installing the bootstrap image, you need a web server, with
the package files available to OpenWRT. You could copy the package
files to the HDD, but I have not tried that. ```/etc/opkg.conf``` need
an adjustment to tell opkg (the package manager) where to find the
packages:

	dest root /
	dest ram /tmp
	lists_dir ext /var/opkg-lists
	option overlay_root /overlay
	src/gz base http://serverip/packages/base
	#src/gz telephony http://serverip/packages/telephony
	src/gz deadbok http://serverip/packages/deadbok
	src/gz packages http://serverip/packages/packages
	src/gz routing http://serverip/packages/routing
	src/gz luci http://serverip/packages/luci
	#src/gz management http://serverip/packages/management
	
Replace ```severip``` with the IP address of the computer serving the
packages.

Update the package index.

	opkg update


Installing required packages.
-----------------------------

*File systems:*

	opkg install kmod-fs-ext4 swap-utils

*Web server:*

	opkg install ca-certificates
	opkg install lighttpd lighttpd-mod-accesslog lighttpd-mod-compress
	
 + ```lighttpd-mod-accesslog```: Log access to the web server to a file.
 + ```lighttpd-mod-compress```: Compress data before sending them to the client.


Installing the optional packages.
----------------------------------

These are just tools that are nice to have.
	
*File manager:*

	opkg install mc
	

*Easy editor*

	opkg install nano


*SFTP server:* 

	opkg install openssh-sftp-server


Installing packages for ssg.
-------------------------------

*Python 3:*

For some reason my package does not pull in the Python 3 dependency
correctly, therefore the package ```python3``` must be installed first.

	opkg install python3
	opkg install python3-setuptools


*Git:*

Links in ```/usr/libexec/git-core/``` are wrong, this is corrected by
creating the symlink, see [Bug #11930](https://dev.openwrt.org/ticket/11930).

	opkg install git
	ln -s $$(which git) /usr/libexec/git-core/git
	

Final configuration.
====================


Mount points.
-------------

*[Fstab Configuration](http://wiki.openwrt.org/doc/uci/fstab)*

OpenWRT uses `/etc/config/fstab` to configure mount points.

 
	config global
		option	anon_swap	'0'
		option	anon_mount	'0'
		option	auto_swap	'1'
		option	auto_mount	'1'
		option	delay_root	'5'
		option	check_fs	'1'

The global section tells OpenWRT, to not mount any drives that to not
have their own sectinoc in fstab (anon_*). Auto_* to mount any file
system and swap space, from the fstab. Delay mounting for 5 seconds,
and perform a file system check if needed. 


	config mount
		option target 		'/mnt/data'
		option fstype 		'ext4'
		option options 		'rw,sync'
		option enabled 		'1'
		option device 		'/dev/sda2'
		option enabled_fsck	'1'
		
This section configures `/dev/sda2` as an ext4 partition with
read-write access, and mounts it at `/mnt/data`.
		
	config swap
		option device 		'/dev/sda3'
		option enabled 		'1'

Last is the swap space from `/dev/sda3'.

Create the mount point and mount the partitions.

	mkdir /mnt/data
	block mount


Configuring lighttpd.
---------------------

*[Configuring Lighttpd](http://redmine.lighttpd.net/projects/lighttpd/wiki/TutorialConfiguration)*,
*[Lighttpd Secure Web Server Tutorial](https://calomel.org/lighttpd.html)*

Configuration is done in `/etc/lighttpd/lighttpd.conf`:

	#Include the accesslog module to log web site access
	server.modules = ( "mod_accesslog" )

	#Root of the webserver is at /mnt/data/www
	server.document-root        = "/mnt/data/www"

	#Where uploaded files are stored	
	server.upload-dirs          = ( "/mnt/data/tmp" )

	#Where errors are logged
	server.errorlog             = "/mnt/data/log/lighttpd/error.log"
	#Process id 
	server.pid-file             = "/var/run/lighttpd.pid"

	#User and group that the server runs as
	server.username             = "http"
	server.groupname            = "www-data"

	#Use index.html if root is requested
	index-file.names            = ( "index.html" )
	#Disable auto index directory listings
	dir-listing.activate     = "disable"

	#Limit request method "POST" size in kilobytes (KB)
	server.max-request-size  = 1

	#Disable multi range requests
	server.range-requests    = "disable"

	#Disable symlinks
	server.follow-symlink    = "disable"

	#Debug options
	debug.log-file-not-found	= "enable"

	#Access log module
	accesslog.syslog-level		= "6"
	accesslog.filename 			= "/mnt/data/log/lighttpd/access.log"

	#Port to bind to
	server.port                 = 80

	include       "/etc/lighttpd/mime.conf"
	#include_shell "cat /etc/lighttpd/conf.d/*.conf"



Adding users and groups.
------------------------




File system permissions.
------------------------

