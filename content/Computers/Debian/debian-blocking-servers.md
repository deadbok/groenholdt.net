author: ObliVion
date: 2016-08-02 03:07
tags: debian, dnsmasq, blocking, lighttpd
title: Blocking domains on local network using dnsmasq on Debian.
template: post

This setup is used on a ECM3610 Debian machine serving as a firewall, 
DHCP server, and DNS server. The following assumes that you have a
working installation something like this:

 * `eth0` is connected to the local (192.168.0.0/24) network.
 * `eth1` is connected to the internet.
 * Shorewall is installed and configured for regular firewall duty.
 * dnsmasq is installed and configured to act as DHCP and DNS server.
 * lighttpd is installed and only exposed on the local network.


Functional description.
=======================

This setup allows requests to a list of domains to be redirected to an
internal web server. Use this setup to block for instance known tracking
servers on the internet.

Somewhere along investigating how to do this I read, in the [ArchWiki
privoxy page](https://wiki.archlinux.org/index.php/privoxy#Ad_Blocking_with_Privoxy)
that blocking trackers creates a unique browser signature. I have
absolutely no reason to doubt this, but there were some servers that I
simply did not want to talk to.


Using dnsmasq to redirect domains.
==================================

dnsmasq.conf:
-------------

If your dnsmasq is configured to listen on an interface, reconfigure it
to use addresses to make stuff prettier when assigning another IP
address to the interface in a little while.

	listen-address=192.168.0.1
	listen-address=127.0.0.1

Use files in /etc/dnsmasq.d/ as configuration files. Uncomment or add
the following:

	conf-dir=/etc/dnsmasq.d/
	
Get a list of servers to block, [http://pgl.yoyo.org/adservers/serverlist.php](http://pgl.yoyo.org/adservers/serverlist.php)
spits out a list formatted for dnsmasq, if you ask it to. The list uses
127.0.0.1 as target, replace it with the address of a local web server
if you want to inform the user that something was blocked, 192.168.0.201
in this case.

	curl -s 'http://pgl.yoyo.org/adservers/serverlist.php?hostformat=dnsmasq&showintro=0&mimetype=plaintext' | sed -r 's/127.0.0.1/192.168.0.201/' > /etc/dnsmasq.d/block2local
	
This could be made into a cron job to update the list from time to time.

Setting up a web server to show an information page.
====================================================

I have lighttpd serving some pages to the local network, so I add
another IP address to eth0, and configure lighttpd to serve this address
from another directory.

interfaces:
-----------

Add this:

	iface eth0 inet static
		address 192.168.0.201
		netmask 255.255.255.0

lighttpd.conf:
--------------

Add this:

	$$SERVER["socket"] == "192.168.0.201:80" {
	   server.document-root = "/var/www/blocked"
	}
	
Add something that serves your purpose to the `server.document-root`
directory. Simplest is something like:

index.html
----------

	<html>
	<head>
	<title>Server blocked.</title>
	</head>
	<body>
	<p>This server is blocked on this network.</p>
	</body>
	</html>

