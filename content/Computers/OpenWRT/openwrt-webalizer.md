author: ObliVion
date: 2015-02-07 16:30
slug: OpenWRT-webalizer
tags: OpenWRT, webalizer
title: The webalizer statistics on OpenWRT
type: post
template: post

(The webalizer)[http://www.webalizer.org/] is a program, that scans web
server log files, and creates statistics from the entries. Since
webalizer uses log files, there are no cookies involved, and webalizer
uses flat files for storage, no database to install. Webalizer is
designed to be run at some interval to update the statistics. 

Installing and configuring.
===========================

	opkg install webalizer
	
To run `webalizer`, create a cron job for it in `/etc/crontab/http`, by
putting the job in the `http` file, cron is told to run it as the `http`
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

	# The Hide*, Group* and Ignore* and Include* keywords allow you to
	# change the way Sites, URLs, Referrers, User Agents and Usernames
	# are manipulated.  The Ignore* keywords will cause The Webalizer to
	# completely ignore records as if they didn't exist (and thus not
	# counted in the main site totals).  The Hide* keywords will prevent
	# things from being displayed in the 'Top' tables, but will still be
	# counted in the main totals.  The Group* keywords allow grouping
	# similar objects as if they were one.  Grouped records are displayed
	# in the 'Top' tables and can optionally be displayed in BOLD and/or
	# shaded. Groups cannot be hidden, and are not counted in the main
	# totals. The Group* options do not, by default, hide all the items
	# that it matches.  If you want to hide the records that match (so just
	# the grouping record is displayed), follow with an identical Hide*
	# keyword with the same value.  (see example below)  In addition,
	# Group* keywords may have an optional label which will be displayed
	# instead of the keywords value.  The label should be separated from
	# the value by at least one 'white-space' character, such as a space
	# or tab.  If the match string contains whitespace (spaces or tabs),
	# the string should be quoted with either single or double quotes.
	#
	# The value can have either a leading or trailing '*' wildcard
	# character.  If no wildcard is found, a match can occur anywhere
	# in the string. Given a string "www.yourmama.com", the values "your",
	# "*mama.com" and "www.your*" will all match.

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

These are impoartant options:

+OutputDir		`/mnt/data/www/stats`
+Incremental	`yes`
	Save state information, so that webalizer will not forget, even if
	the logs are cleared.
+HostName		`groenholdt.net`
	The host name of your server.
+OmitPage		`/stats/`
	Do not keep statistics of the statistics.
+HideSite	`*groenholdt.net`
+HideSite	`localhost`
+HideReferrer	groenholdt.net/
	Hide access from oneself from the "Top" lists. 
	
Make the configuration file readable to all users.

	chmod a+r /etc/webalizer.conf 

Create the directories, and set user `http`, group `www-data` as owner.
Make the directory writable by all members of the group `www-data`. This
is done so that both lighttpd and The Webalizer have permission to
access the files. 

	mkdir -p /mnt/data/www/stats/
	chown http:www-data /mnt/data/www/stats -R
	chmod g+w /mnt/data/www/stats -R

To restrict access to webalizer to computers on the local network, add
these lines to `/etc/lighttpd/lighttpd.conf`:

	# Deny the access to statistics to all user which 
    # are not in the 192.168.0.x network
    $$HTTP["remoteip"] !~ "^(192\.168\.0\.)" {
      $$HTTP["url"] =~ "^/stats/" {
        url.access-deny = ( "" )
      }
    }

Replace `"^(192\.168\.0\.)"` with an IP address matching your network.
