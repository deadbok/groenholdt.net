author: ObliVion
date: 2015-02-27 16:215
slug: OpenWRT-logrotate
tags: OpenWRT, logrotate
title: Rotating lighhtpd logs on OpenWRT
type: post
template: post

With the current setup, if no maintenance is done, the log files from
lighhtpd will just keep on growing. OpenWRT itself is configured to
rotate its log files once they grow beyond 1MB. This is pretty nice, and
since webalizer is configured to cope with disappearing log entries, it
would be nice to rotate the web server log as well. To do this, install
`logrotate`.

	opkg install logrotate
	
`logrotate` has a global configuration file in `/etc/logrotate.conf`,
and for individual programs in the directory `/etc/logrotate.d/`. Read
the man page at [Ubuntu Manpage: logrotate](http://manpages.ubuntu.com/manpages/saucy/en/man8/logrotate.8.html)
on the use of `logrotate` and the syntax of the configuration files. To 
rotate the log files of lighttpd, add the file `/etc/logrotate.d/lighttpd`,
with the following contents:

	/mnt/data/log/lighttpd/access.log {
		weekly
		rotate = 53
		su http www-data
		postrotate
			/usr/bin/killall -HUP  lighttpd        
		endscript
	}

This tells logrotate to rotate lighttpd logs, every week, and keep about
a years worth of log files. The log files needs to be accessed as user 
`http`, and group `www-data`, and lighttpd is told to create a new log
file by sending it the SIGHUP signal.

`logrotate` needs to be run daily, so set up a cron job for it. Add the 
following to run logrotate once a day at 8:00.

 0 8 * * * *     /usr/sbin/logrotate -s /mnt/data/tmp/logrotate.state /etc/logrotate.conf
  
