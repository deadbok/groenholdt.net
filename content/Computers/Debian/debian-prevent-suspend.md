author: ObliVion
date: 2015-03-10 20:05
tags: Debian, Debian testing, suspend, systemd
title: Preventing Debian testing from suspending.
type: post
template: post


My Acer Aspire One D250, kept going into suspend every minute or so, 
whenever I was not logged in to a window manager. I run Debian testing
and had my first real interaction with systemd (except for systemctl).

Turns out there are some settings in `/etc/systemd/logind.conf` that
configures some of the power management features.

	#  This file is part of systemd.
	#
	#  systemd is free software; you can redistribute it and/or modify it
	#  under the terms of the GNU Lesser General Public License as published by
	#  the Free Software Foundation; either version 2.1 of the License, or
	#  (at your option) any later version.
	#
	# See logind.conf(5) for details

	[Login]
	#NAutoVTs=6
	#ReserveVT=6
	#KillUserProcesses=no
	#KillOnlyUsers=
	#KillExcludeUsers=root
	#InhibitDelayMaxSec=5
	HandlePowerKey=poweroff
	HandleSuspendKey=ignore
	HandleHibernateKey=ignore
	HandleLidSwitch=ignore
	#PowerKeyIgnoreInhibited=no
	#SuspendKeyIgnoreInhibited=no
	#HibernateKeyIgnoreInhibited=no
	#LidSwitchIgnoreInhibited=yes
	IdleAction=ignore
	#IdleActionSec=30min
	#RuntimeDirectorySize=10%
	#RemoveIPC=yes

First I asked systemd to ignore everything but the power button, and
as I somewhat expected this didn't do the trick. Then I set the `IdleActionSec`
to the actual amount of second (1800), that didn't work either. In the
end completely disabling idling, stopped the suspend.

	IdleAction=ignore
