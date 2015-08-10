author: ObliVion
date: 2015-08-08 10:25
status: hidden
tags: debian, web server
title: Debian web server software
template: post

Debian web server software
==========================

Generic software
---------------

 * Lighttpd
 * Webalizer
 * Logwatch
 * Logrotate
 * sSMTP
 * anacron
  
Service specific software
-------------------------
 * Python
 * Flask
 * Python-psutil
 * Git
 * ssg
 * server-hud
 * Gunicorn
 * Chromium
 * LightDM

Configuration snippets
======================

sSMTP and GMail
---------------

	mailhub=smtp.gmail.com:587
	hostname=HOST NAME
	AuthMethod=LOGIN
	AuthUser=YOU@gmail.com
	AuthPass=PASSWORD
	useSTARTTLS=YES
