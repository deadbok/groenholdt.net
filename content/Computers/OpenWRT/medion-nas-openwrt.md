author: ObliVion
date: 2015-02-06 17:49
slug: OpenWRT-web-server-medion-OX820-based-NAS
tags: OpenWRT, NAS, Medion MD86517, web server
title: Installing an OpenWRT based webserver on the Medion OX820 based NAS 
type: post
template: post

After getting Gentoo to run on the Medion NAS in these posts,

 + [Medion OX820 based NAS and Gentoo]($LOCALURL/../Gentoo/medion-0x820-based-nas/medion-ox820-based-nas.html)
 + [Medion NAS native kernel compile]($LOCALURL/../Gentoo/medion-nas-native-kernel-compile.html)

I learned that [OpenWRT](http://openwrt.org) had been ported to the oxnas platform. This 
appealed to me, as OpenWRT is installed on the internal flash. Honestly
the Gentoo installation I had on the HDD, was better suited as a web
server, but I just wanted to play with OpenWRT. The only real reason for 
using OpenWRT instead of Gentoo, is in the hopes that the OpenWRT folks 
will keep the kernel updated.

I still have my web page, and the files from which it is generated, on
a hard disk drive, connected to the SATA port.

I recommend having a serial connection to the NAS running at all times.

Installing OpenWRT bootstrap.
=============================

This operation can only be executed once, and **may brick your device**,
after the bootstrap **there is no way to restore the original firmware**.
Because of this I can not actually check that these steps are exactly
right, but they are what i recall.

To bootstrap the installation I used the 
[binary image](https://gitorious.org/openwrt-oxnas/openwrt-oxnas-gitorious-wiki/archive/2e5653b2c09ed9dca988f89c68f44a61e3bdde19.tar.gz) 
from
[Gitorious openwrt-oxnas](https://gitorious.org/openwrt-oxnas/pages/install).

Setup a HTTP server on a computer to serve `openwrt-oxnas-stg212-u-boot-initramfs.itb`.
Telnet into the NAS using the backdoor described on 
 [mikrocontroller.net](http://www.mikrocontroller.net/articles/P89626#Telnet).
Login to the web-interface on the NAS, then open 
`http://(NAS IP)/r36807,/adv,/cgi-bin/remote_help-cgi?type=backdoor`
(you may have to replace the /rXXXXX,/ with the revision number shown 
in the URL after login).
The browser will wait for the CGI script to (never) end, while it’s 
doing that telnet into the NAS. Login with user root and the password
also used by the web interface (default is 1234).

	telnet (NAS IP)

After logging in, download the OpenWRT image to `/tmp/tmpfs`. Look in
`/proc/mtd` and make sure `kernel` is in `/dev/mtd4`. Write the image
to `/dev/mtd4`, tell U-Boot to boot from it, and reboot. 

	cd /tmp/tmpfs wget http://(server IP)/openwrt-oxnas-stg212-u-boot-initramfs.itb
	cat /proc/mtd 
	nandwrite /dev/mtd4 openwrt-oxnas-stg212-u-boot-initramfs.itb 
	fw_setenv boot_stage2 nand read 64000000 440000 90000\\; go 64000000
	fw_setenv bootcmd run boot_stage2 reboot

This is where the serial connection comes in handy, for watching the
boot process. If everything went well LUCI, OpenWRT's web interface
should be available on the NAS on address 192.168.1.1. When you have
compiled a new OpenWRT image you can flash it, by using LUCI.

Building OpenWrt.
==================
*[OpenWrt Buildroot – About](http://wiki.openwrt.org/about/toolchain).*

Since, for now, oxnas support is only in OpenWRT trunk, everything needs
to be build.

I build this on a [Gentoo](http://gentoo.org/) system, which seems to 
need automake-1.14 installed for glib2 to build.

Getting the sources.
--------------------

Change into the directory where you want the sources to reside and do:

    git clone git://git.openwrt.org/openwrt.git 
    cd openwrt

OpenWRT uses 

To have the standard set of packages available for OpenWRT copy 
`feeds.conf.default` to `feeds.conf`.

	cp feeds.conf.default feeds.conf

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


Update and add the feeds.
-------------------------

Add the packages to the build system.

	./scripts/feeds update -a
	./scripts/feeds install -a
    

Configuring the sources.
------------------------

I have configured a lot of stuff, that I am not using right now, as 
modules, so that I can later install them if I find a need. This
increases the build time, so it is a trade off compared to building
just the packages that you want right now.
You can download my [configuration file]($LOCALURL/openwrt-config),
and use it as a basis for your own configuration.

	wget $LOCALURL/openwrt-config
	mv openwrt-config .config

To configure the OpenWRT build run `make menuconfig` in the  source
directory.

I can not describe every configuration option, but here are some 
important ones.

First to build OpenWRT for the NAS these tell the build system about the
basic hardware:


	Target System (PLXTECH/Oxford NAS782x/OX82x)
	Target Profile (MitraStar STG-212)

Under `Target Images` select 

+ `ubifs` is the filesystem of the images we will be building for the NAS.

+ `ramdisk` I always build a ramdisk as well, since it can be used to unbrick the 
	device, if you can still access the boot loader through the serial
	connection. Under `Target Imaqes` -> `ramdisk` make sure `xz` 
	compression is selected.

Under `Global build settings` I enable at least

+ `Enable shadow password support` to have encrypted passwords for 
	users in `/etc/shadow`.
	
+ `Support for paging of anonymous memory (swap)` To enable swap
	functionality in the kernel.
	
+ I disable all kernel debugging features, as this is a production
	environment.
	
If you want to develop or debug the build process of packages in 
OpenWRT enable `Advanced configuration options (for developers)`, 
some sub-options that I use are:

+ `Automatic rebuild of packages` rebuilds packages when their files
	changes.
	
+ `Enable log files during build process` log build output in files
	under `log/`.

Under `Base system`

+ `ca-certificates` build as a module for STFP.

+ Enable the `firewall` as you might want to close everything to the
  outside.

+ `busybox` is customized for the multi user setup we will do later.
	+ `Customize busybox options` enabled.
		+ `Busybox Settings`.
			+ `General Configuration`.
				+ `Support Unicode` enabled to be on the safe side.
				+ `Support for SUID/SGID handling` needed for the su
				   command.
		+ `Coreutils`.
			+ `groups`, `id`, `chmod`, `chown` enabled.
		+ `Login/Password Management Utilities`.
			+ `Support for shadow passwords` same as earlier.
			+ `Use internal password and group functions rather than system functions`
			  enabled.
				+ `Use internal shadow password functions` enabled, 
				  to use busybox functions instead of the `shadow`
				  package.
			+ `adduser`, `addgroup`, `deluser`, `delgroup`, `passwd`, enabled.
			+ `su`, enabled.
				+ `Enable su to write to syslog`, enabled. Root access 
				  will be logged.
		+ `Miscellaneous Utilities`.
			+ `crond` which I think it is enabled by default.
			+ `crontab` which I think it is enabled by default.
			
In `Kernel modules` I believe that everything needed is enabled by 
default, but there is a little more stuff that is nice.

+ Block Devices
	+ `kmod-loop` as module. Loop devices are so neat.
+ `Filesystems` enable whatever you may need.
+ `LED modules` these might be fun.

In `Languages` I enable `python3` and `setuptools` for my
static site generator.

In `LuCI` make sure to enable the basic interface and build it as a 
module. LuCI is the only reliable way I have been able to flash a new
image to the NAS.

In `Network` a lot of things like web servers hide.

+ `File Transfer`, I have `curl`, `rsync` and `wget` compiled as modules.
+ `SSH` enable `openssh-sftp-server` for SFTP access.
+ `Web Serves/Proxies` enable a web server, here I use `lighttpd`. 
  enable `webalizer` if you want site statistics.
				  
Compile.
--------
The CA-certificates package expect `python` to point to a python 2.x
interpreter, my Gentoo system uses Python 3, which leads to missing
certificates. I made a [patch]($LOCALURL/100-use-python2.patch), that
you can drop into `packages/system/ca-certificates/patches` in your
OpenWRT directory, if you run into this.

To build everything just run `make`. To see all output from the build 
process use: 

	make V=s

The images en up in `bin/oxnas`, along with the packages. I flash 
`openwrt-oxnas-stg212-ubifs-sysupgrade.tar` using LuCI.


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

Like when installing the bootstrap image you need a web server with
the package files available to OpenWRT. I assume that the OpenWRT
package tree is copied to the root of the server. You could copy the package
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

	opkg install kmod-fs-ext4 swap-utils opkg e2fsprogs
	modprobe ext4

*Web server:*

	opkg install ca-certificates
	opkg install lighttpd lighttpd-mod-accesslog lighttpd-mod-compress
	opkg install lighttpd-mod-status lighttpd-mod-alias
	
 + ```lighttpd-mod-accesslog```: Log access to the web server to a file.
 + ```lighttpd-mod-compress```: Compress data before sending them to the client.
 +`lighttpd-mod-status`: Publishes some status information about the server.
 +`lighttpd-mod-alias`: Allows you to point an URL at a specific directory.
 
*Web server statistics:*

	opkg install webalizer


Installing the optional packages.
----------------------------------

These are just tools that are nice to have.
	
*File manager:*

	opkg install mc
	

*Easy editor*

	opkg install nano


*SFTP server:* 

	opkg install openssh-sftp-server
	
*USB mass storage support (aka. USB stick)*

	opkg install kmod-usb-storage-extras


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

System.
-------

*[System configuration](http://wiki.openwrt.org/doc/uci/system)*

Global configuration is done in `/etc/config/system`. I sent the logs to
a file on the HDD, and limited it at 1Mb in size. You should configure 
the host name and time zone to your local preferences.

The log levels of different subsystems is configured in this file as 
well. *Notice that for `conloglevel` and `klogconloglevel` a higher
number means more verbose, while for `cronloglevel` it is the other way
around.* 

I have not touched the time server configuration, I only use the client
part, and it worked out of the box.

	config system
			option hostname         OpenWRT
			option log_file         /mnt/data/log/messages
			option log_size         1024
			option log_type         file
			option timezone         Europe/Copenhagen
	#Log levels 1-8
	#Higher is more verbose
			option conloglevel      4
	#Lower is more verbose
			option cronloglevel     4

	config timeserver ntp
			list server             0.openwrt.pool.ntp.org
			list server             1.openwrt.pool.ntp.org
			list server             2.openwrt.pool.ntp.org
			list server             3.openwrt.pool.ntp.org
			option enabled          1
			option enable_server    0


Mount points.
-------------

*[Fstab Configuration](http://wiki.openwrt.org/doc/uci/fstab)*

There are two "disks" in the system, the internal flash, and the HDD
connected to the SATA port.

 + ```/``` OpenWRT on the internal flash.
 + ```/mnt/data``` Root of the connected HDD.
 + ```/mnt/data/www``` Root of the pages served by lighttpd.
 + ```/mnt/data/log``` System log files.
 + ```/mnt/data/tmp``` Temporary files.

OpenWRT uses `/etc/config/fstab` to configure mount points.
 
	config global
		option	anon_swap	'0'
		option	anon_mount	'0'
		option	auto_swap	'1'
		option	auto_mount	'1'
		option	delay_root	'5'
		option	check_fs	'1'

The global section tells OpenWRT, to not mount any drives that do not
have their own section in fstab (anon_*). Auto_* to mount any file
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
	
Create directories for web server, logs, and temporary files.

	mkdir /mnt/data/{www,log,tmp}



Adding users and groups.
------------------------

OpenWRT is not build to be a multiuser system, but it is possible to
configure it like that. There are two options, either use `shadow` like
a desktop Linux system, or use busybox build in user handling. I have
used the busybox version, since it is lighter.

User directories are kept on the HDD and linked into the root file
system.

	mkdir -p /mnt/data/home
	ln -sf /mnt/data/home /home

Users are added using the `adduser` command. Replace `username` with
the user name you want.

	adduser username

Next create the user directory and set the permissions.

	mkdir /mnt/data/home/username
	chown -R username /mnt/data/home/username
	chmod 700 /mnt/data/home/username

I still want root access, but I to log in as a regular user and `su` to
the root account, like a desktop system. Busybox needs some setup for 
the `su` command to work.
	
	chmod u+s /bin/busybox

`/etc/busybox.conf`

	[SUID]
	su = ssx root.root
	

Disabling root access from ssh.
-------------------------------

*[Dropbear Configuration](http://wiki.openwrt.org/doc/uci/dropbear)*

Now that `su` works, there is no reason to allow root access through 
ssh, if you do not need ssh it would be even better to disable it.


For non root access:
`/etc/config/dropbear`

	config dropbear
		option PasswordAuth 	'1'
		option RootPasswordAuth '0'
		option RootLogin		'0'
		option Port         	'22'

Disable ssh enterily:

	/etc/init.d/dropbear disable


File system permissions.
------------------------

Permissions for `/mnt/data/www/`, the directory served by lighttpd.

	chown http:www-data /mnt/data/www/


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
	
I have disabled symlinks in this configuration, which means that the 
web root directory, cannot be a symlink. You will get something like 
`403 Forbidden` if you try. The same goes for symlinks inside the web
root directory, they won't work.

You can change this behavior by changing `server.follow-symlink = "disable"`
to `server.follow-symlink = "enable"`, but i encourage you to read
[this answer on Server Fault](http://serverfault.com/questions/244592/followsymlinks-on-apache-why-is-it-a-security-risk/244612#244612).

Enable lighttpd at boot.

	/etc/init.d/lighttpd enable
	

The Webalizer, web site statistiscs.
------------------------------------
*(The webalizer)[http://www.webalizer.org/]*

To run `webalizer`, create a cron job for it in `/etc/crontab/http`, by
putting the jop in the `http` file, cron is told to run it as the `http`
user.

	0 */12 * * * /usr/bin/webalizer -q
	
There is a thoroughly commented config file in `/etc/webalizer.conf.sample`,
to use this as a the base for your changes, copy the file to `/etc/webalizer.conf`.
	
	cp /etc/webalizer.conf.sample /etc/webalizer.conf
	
Here is my configuration:

	#
	# Webalizer configuration file
	#

	# LogFile defines the web server log file to use.  If not specified
	# here or on on the command line, input will default to STDIN.  If
	# the log filename ends in '.gz' (a gzip compressed file), or '.bz2'
	# (bzip2 compressed file), it will be decompressed on the fly as it
	# is being read.

	LogFile        /mnt/data/log/lighttpd/access.log

	# OutputDir is where you want to put the output files.  This should
	# should be a full path name, however relative ones might work as well.
	# If no output directory is specified, the current directory will be used.

	OutputDir      /mnt/data/www/stats

	# HistoryName allows you to specify the name of the history file produced
	# by the Webalizer.  The history file keeps the data for previous months,
	# and is used for generating the main HTML page (index.html). The default
	# is a file named "webalizer.hist", stored in the output directory being
	# used.  The name can include a path, which will be relative to the output
	# directory unless absolute (starts with a leading '/').

	HistoryName	webalizer.hist

	# Incremental processing allows multiple partial log files to be used
	# instead of one huge one.  Useful for large sites that have to rotate
	# their log files more than once a month.  The Webalizer will save its
	# internal state before exiting, and restore it the next time run, in
	# order to continue processing where it left off.  This mode also causes
	# The Webalizer to scan for and ignore duplicate records (records already
	# processed by a previous run).  See the README file for additional
	# information.  The value may be 'yes' or 'no', with a default of 'no'.
	# The file 'webalizer.current' is used to store the current state data,
	# and is located in the output directory of the program (unless changed
	# with the IncrementalName option below).  Please read at least the section
	# on Incremental processing in the README file before you enable this option.

	Incremental	yes

	# IncrementalName allows you to specify the filename for saving the
	# incremental data in.  It is similar to the HistoryName option where the
	# name is relative to the specified output directory, unless an absolute
	# filename is specified.  The default is a file named "webalizer.current"
	# kept in the normal output directory.  If you don't specify "Incremental"
	# as 'yes' then this option has no meaning.

	IncrementalName	webalizer.current

	# HostName defines the hostname for the report.  This is used in
	# the title, and is prepended to the URL table items.  This allows
	# clicking on URLs in the report to go to the proper location in
	# the event you are running the report on a 'virtual' web server,
	# or for a server different than the one the report resides on.
	# If not specified here, or on the command line, webalizer will
	# try to get the hostname via a uname system call.  If that fails,
	# it will default to "localhost".

	HostName	groenholdt.net

	# PageType lets you tell the Webalizer what types of URLs you
	# consider a 'page'.  Most people consider html and cgi documents
	# as pages, while not images and audio files.  If no types are
	# specified, defaults will be used ('htm*', 'cgi' and HTMLExtension
	# if different for web logs, 'txt' for ftp logs).

	PageType	htm*
	PageType	cgi
	#PageType	phtml
	#PageType	php3
	#PageType	pl

	# OmitPage lets you tell the Webalizer that certain URLs do not
	# contain any pages.  No URL matching an OmitPage value will be
	# counted as a page, even if it matches a PageType above or has
	# no extension (e.g., a directory).  They will still be counted
	# as a hit.

	OmitPage	/stats/

	# UseHTTPS should be used if the analysis is being run on a
	# secure server, and links to urls should use 'https://' instead
	# of the default 'http://'.  If you need this, set it to 'yes'.
	# Default is 'no'.  This only changes the behaviour of the 'Top
	# URLs' table.

	#UseHTTPS       no

	# DNSCache specifies the DNS cache filename to use for reverse DNS lookups.
	# This file must be specified if you wish to perform name lookups on any IP
	# addresses found in the log file.  If an absolute path is not given as
	# part of the filename (ie: starts with a leading '/'), then the name is
	# relative to the default output directory.  See the DNS.README file for
	# additional information.

	DNSCache	dns_cache.db

	# DNSChildren allows you to specify how many "children" processes are
	# run to perform DNS lookups to create or update the DNS cache file.
	# If a number is specified, the DNS cache file will be created/updated
	# each time the Webalizer is run, immediately prior to normal processing,
	# by running the specified number of "children" processes to perform
	# DNS lookups.  If used, the DNS cache filename MUST be specified as
	# well.  The default value is zero (0), which disables DNS cache file
	# creation/updates at run time.  The number of children processes to
	# run may be anywhere from 1 to 100, however a large number may affect
	# normal system operations.  Reasonable values should be between 5 and
	# 20.  See the DNS.README file for additional information.

	DNSChildren	8

	# CacheIPs allows unresolved IP addresses to be cached in the DNS
	# database.  Normally, only resolved addresses are saved.  At some
	# sites, particularly those with a large number of unresolvable IP
	# addresses visiting, it may be useful to enable this feature so
	# those addresses are not constantly looked up each time the program
	# is run.  Values can be 'yes' or 'no', with 'no' being the default.

	CacheIPs	yes

	# CacheTTL specifies the time to live (TTL) value for cached DNS
	# entries, in days.  This value may be anywhere between 1 and 100
	# with the default being 7 days (1 week).

	#CacheTTL	7

	# The GeoDB option enables or disabled the use of the native
	# Webalizer GeoDB geolocation services.  This is the preferred
	# geolocation option.  Values may be 'yes' or 'no', with 'no'
	# being the default.

	#GeoDB		no

	# GeoDBDatabase specifies an alternate database to use.  The
	# default database is /usr/share/GeoDB/GeoDB.dat (however the
	# path may be changed at compile time; use the -vV command
	# line option to determine where).  If a different database is
	# to be used, it may be specified here.  The name is relative
	# to the output directory being used unless an absolute name
	# (ie: starts with a leading '/') is specified.

	#GeoDBDatabase	/usr/share/GeoDB/GeoDB.dat

	# The GeoIP option enables or disables the use of geolocation
	# services provided by the GeoIP library (http://www.maxmind.com),
	# if available.  Values may be 'yes' or 'no, with 'no' being the
	# default.  Note: if GeoDB is enabled, then this option will have
	# no effect (GeoDB will be used regardless of this setting).

	#GeoIP		no

	# GeoIPDatabase specifies an alternate database filename to use by the
	# GeoIP library.  If an absolute path is not given as part of the name
	# (ie: starts with a leading '/'), then the name is relative to the
	# default output directory. This option should not normally be needed.

	#GeoIPDatabase	/usr/share/GeoIP/GeoIP.dat

	# VisitTimeout allows you to set the default timeout for a visit
	# (sometimes called a 'session').  The default is 30 minutes,
	# which should be fine for most sites.
	# Visits are determined by looking at the time of the current
	# request, and the time of the last request from the site.  If
	# the time difference is greater than the VisitTimeout value, it
	# is considered a new visit, and visit totals are incremented.
	# Value is the number of seconds to timeout (default=1800=30min)

	#VisitTimeout	1800

	# The All* keywords allow the display of all URLs, Sites, Referrers
	# User Agents, Search Strings and Usernames.  If enabled, a separate
	# HTML page will be created, and a link will be added to the bottom
	# of the appropriate "Top" table.  There are a couple of conditions
	# for this to occur..  First, there must be more items than will fit
	# in the "Top" table (otherwise it would just be duplicating what is
	# already displayed).  Second, the listing will only show those items
	# that are normally visable, which means it will not show any hidden
	# items.  Grouped entries will be listed first, followed by individual
	# items.  The value for these keywords can be either 'yes' or 'no',
	# with the default being 'no'.  Please be aware that these pages can
	# be quite large in size, particularly the sites page,  and separate
	# pages are generated for each month, which can consume quite a lot
	# of disk space depending on the traffic to your site.

	#AllSites	no
	#AllURLs	no
	#AllReferrers	no
	#AllAgents	no
	AllSearchStr	yes
	#AllUsers       no

	# Your own site should be hidden
	HideSite	*groenholdt.net
	HideSite	localhost

	# Your own site gives most referrals
	HideReferrer	groenholdt.net/

	# Usually you want to hide these
	HideURL		*.gif
	HideURL		*.GIF
	HideURL		*.jpg
	HideURL		*.JPG
	HideURL		*.png
	HideURL		*.PNG
	HideURL		*.ra

	# The MangleAgents allows you to specify how much, if any, The Webalizer
	# should mangle user agent names.  This allows several levels of detail
	# to be produced when reporting user agent statistics.  There are six
	# levels that can be specified, which define different levels of detail
	# supression.  Level 5 shows only the browser name (MSIE or Mozilla)
	# and the major version number.  Level 4 adds the minor version number
	# (single decimal place).  Level 3 displays the minor version to two
	# decimal places.  Level 2 will add any sub-level designation (such
	# as Mozilla/3.01Gold or MSIE 3.0b).  Level 1 will attempt to also add
	# the system type if it is specified.  The default Level 0 displays the
	# full user agent field without modification and produces the greatest
	# amount of detail.  User agent names that can't be mangled will be
	# left unmodified.

	#MangleAgents    0

	# The SearchEngine keywords allow specification of search engines and
	# their query strings on the URL.  These are used to locate and report
	# what search strings are used to find your site.  The first word is
	# a substring to match in the referrer field that identifies the search
	# engine, and the second is the URL variable used by that search engine
	# to define its search terms.

	#SearchEngine	.google.   	q=
	#SearchEngine	yahoo.com	p=
	#SearchEngine	altavista.com	q=
	#SearchEngine   aolsearch.      query=
	#SearchEngine   ask.co          q=
	#SearchEngine	eureka.com	q=
	#SearchEngine	lycos.com	query=
	#SearchEngine	hotbot.com	MT=
	#SearchEngine	msn.com		q=
	#SearchEngine	infoseek.com	qt=
	#SearchEngine	excite		search=
	#SearchEngine	netscape.com	query=
	#SearchEngine	mamma.com	query=
	#SearchEngine	alltheweb.com	q=
	#SearchEngine	northernlight.com  qr=

	# End of configuration file...  Have a nice day!

	
Make the configuration file readable to all users.

	chmod a+r /etc/webalizer.conf 

Create the directories, and set user `http`, group `www-data` as owner.
Make the directory writable by all members of the group `www-data`. This
is done so that both lighttpd and The Webalizer have permission to
access the files. 

	mkdir -p /mnt/data/www/stats/
	chown http:www-data /mnt/data/www/stats -R
	chmod g+w /mnt/data/www/stats -R
	
To not have search bots index the statistics, create a `/mnt/data/www/robots.txt` 
file with the following contents.

	User-agent: *
	Disallow: /stats
