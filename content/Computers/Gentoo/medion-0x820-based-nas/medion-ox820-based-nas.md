author: ObliVion
date: 2014-05-21 20:00
slug: medion-OX820-based-NAS-and-gentoo
tags: Gentoo, NAS, Medion MD86517, web server
title: Medion OX820 based NAS and Gentoo
type: post
template: post


I was given a [Medion MD86517 NAS](http://www.mikrocontroller.net/articles/P89626) 
without a drive for free. I wanted to put a 2.5" disk in it, and use it as a 
web-server. The NAS runs Linux, and the sources are [here](http://download2.medion.com/downloads/software/gpl_source_md86407.exe).

A large part of the installation was done on a regular Gentoo x86/x64 PC,
using a SATA to USB converter. Start with a clean drive
with no partitions, connected to the host computer (Not the NAS). 

During the install, I have aimed to have all files needed for a new intall,
located on the NAS drive itself, in the hopes that it will make a reinstall,
easier. You can of course remove these files from ``/usr/src``, if you do not
want this.

!{The serial port connection}($LOCALURL/nas_serial_port.png)

*Much of this stuff needs root permissions, and all the NAS side stuff is done
through a serial connection.* If something is unclear, read [The Gentoo handbook](http://www.gentoo.org/doc/en/handbook/),
this is in esence the same procedure, except I boot into the system instead of
chrooting.

A lot of thanks and credit to the people in [this thread](http://archlinuxarm.org/forum/viewtopic.php?f=55&t=6193),
without whom I would never have gotten on the right track.

Partitioning
============

To boot from the SATA disk, a special partition layout is needed. The ox820
reads the start of the drive, to check if it is bootable. A script has been
written to put the right data in the first part of the hard disk.
Download [disk creation files]($LOCALURL/onax-sata_boot.tar.gz) created by 
[WarheadsSE](https://github.com/WarheadsSE), extract the files somewhere, and 
enter that directory. **Edit the disk_create script to change the target drive 
in the variable ``disk``.**

Creating the partitions
-----------------------

Prepare the disk using WarheadsSE's tool.

    ./disk_create

Fire up fdisk to partition the disk.

    fdisk -c=dos /dev/sdb

- Create a small partition for U-Boot, stage1, and the kernel. WarheadsSE
  recommends a 10M partition. **This partition must start at sector 2048.**
 
- Create a second partition for the root file system, leave a little space
  left for a swap partition.

- Create a third partition for swap space. Set it as swap type.
    
    
Format the second and third partition, I use ext4 as the root file system.

    mkfs.ext4 /dev/sdb2
    mkswap /dev/sdb3
 
Last, mount the second partition to /mnt/gentoo, your partition may have another
designation than ``/dev/sdb``.

    cd /mnt
    mkdir gentoo
    mount /dev/sdb2 /mnt/gentoo
 

Root file system
================

Download a [stage 3 Gentoo for ARM5](http://mirrors.nl.kernel.org/gentoo//releases/arm/autobuilds/current-stage3-armv5tel/stage3-armv5tel-20140115.tar.bz2),
and extract it to /mnt/gentoo. Though the processor is ARM6 compatible, I could
not get it to boot beyond the kernel using and ARM6 stage 3.

    tar -xvjpf stage3-armv5tel-20140115.tar.bz2 -C /mnt/gentoo

Set the baud rate in /mnt/gentoo/etc/inittab to 115200. Change:

    #s0:12345:respawn:/sbin/agetty -L 9600 ttyS0 vt100

to:

    s0:12345:respawn:/sbin/agetty -L 115200 ttyS0 vt100

Copy ``resolv.conf`` from your host ``/etc`` directory, to have DNS working.

    cp -L /etc/resolv.conf /mnt/gentoo/etc/resolv.conf
  
Create a link from ``net.lo`` to ``net.eth0`` to enable the network at first
boot.

    cd /mnt/gentoo/etc/init.d
    ln -sf net.lo net.eth0

Edit ``/mnt/gentoo/etc/fstab`` to set the devices for the root and swap file
system. The file should contain something like this:

    #/dev/BOOT              /boot           ext2            noauto,noatime  1 2
    /dev/sda2               /               ext4            noatime         0 1
    /dev/sda3               none            swap            sw              0 0
    #/dev/cdrom             /mnt/cdrom      auto            noauto,ro       0 0
    #/dev/fd0               /mnt/floppy     auto            noauto          0 0

Copy passwd and shadow from the running system to have your logins and passwords
when you boot the NAS.

    cp /etc/passwd /mnt/gentoo/etc/passwd
    cp /etc/shadow /mnt/gentoo/etc/shadow
    cp /etc/group /mnt/gentoo/etc/group
  
Select mirrors for portage.

    mirrorselect -i -o >> /mnt/gentoo/etc/portage/make.conf
    mirrorselect -i -r -o >> /mnt/gentoo/etc/portage/make.conf
  
Set the timezone.

    echo "Europe/Copenhagen" > /mnt/gentoo/etc/timezone

Set the hostanme.

    nano -w /mnt/gentoo/etc/conf.d/hostname
    nano -w /mnt/gentoo/etc/hosts

Set the keymap (just in case).

    nano -w /mnt/gentoo/etc/conf.d/keymaps

Last edit and change ``UTC`` to local if needed.

    nano -w /etc/conf.d/hwclock

    
Kernel
======

You will need an ARM cross-compiler, Gentoo's ``crossdev`` comes in handy.

    crossdev -t armv5tel-softfloat-linux-gnueabi

Clone [linux-oxnas](https://github.com/kref/linux-oxnas) into 
``/mnt/gentoo/usr/src``.
  
    cd /mnt/gentoo/usr/src
    git clone https://github.com/kref/linux-oxnas
    ln -sf linux-oxnas linux

    cd linux-oxnas
    make ARCH=arm ox820_defconfig CROSS_COMPILE=armv5tel-softfloat-linux-gnueabi-
    make ARCH=arm menuconfig CROSS_COMPILE=armv5tel-softfloat-linux-gnueabi-

    Boot options --->
    [*] Use appended device tree blob to zImage (EXPERIMENTAL)
    [*] Supplement the appended DTB with traditional ATAG information
    disable PCI support if you device does not have one
  
Remember to compile in support for the root file system type, if you did like me
this means enabling the ext4 file system.

    File system  --->
    <*> The Extended 4 (ext 4) filesystem

Compile and create kernel image.

    make ARCH=arm zImage ox820-pogoplug-pro.dtb CROSS_COMPILE=armv5tel-softfloat-linux-gnueabi-

    cat arch/arm/boot/zImage arch/arm/boot/dts/ox820-pogoplug-pro.dtb > arch/arm/boot/zImage.fdt

    scripts/mkuboot.sh -A arm -O linux -C none -T kernel -a 0x60008000 -e 0x60008000 -n 'Linux-3.11.1+' -d arch/arm/boot/zImage.fdt arch/arm/boot/uImage


Final disk creation
===================

Copy WarheadsSE's disk creation files (contents of onax-sata-boot.tar.gz) to the ``/mnt/gentoo/usr/src``.

    mkdir /mnt/gentoo/usr/src/disk_create
    cp -Rv (Where you unpacked the files)/* /mnt/gentoo/usr/src/disk_create
  
Integrate the new kernel into WarheadsSE's tool.

    cd /mnt/gentoo/usr/src/disk_create
    cp /mnt/gentoo/usr/src/linux-oxnas/arch/arm/boot/uImage uImages/gentoo
    rm uImage
    ln -sf uImages/gentoo uImage
    ./disk_create

Preparing for first boot
========================

Unmount and sync the disk.

    cd /
    umount /mnt/gentoo
    sync

Remove the drive from the host computer and physically install it in the NAS.


First Boot
==========

Set the clock. MMDDhhmmCCYY is month, date, hour, minute, century, year

    date MMDDhhmmCCYY 
 
Get the portage tree.

    emerge --sync
  
Set the Profile.

    eselect profile list

I selected ``default/linux/arm/13.0/armv5te``.

    eselect profile set 18
  
Configure the locales, first put the locales you want supported in ``locale.gen``.
  
    nano -w /etc/locale.gen

Generate the locales and select the system-wide one.
  
    locale-gen
    eselect locale list
    eselect locale set *locale nr.*
    env-update && source /etc/profile
  
Add the network interface to the startup.

    rc-update add net.eth0 default

Update and install some needed stuff.

    emerge -uDNv world ntp cronie syslog-ng openssh logrotate dhcpcd
 
Add it to the startup.

    rc-update add syslog-ng default
    rc-update add cronie default
    rc-update add sshd default
    rc-update add ntp-client default
    rc-update add swclock boot
    rc-update del hwclock boot

The end
=======

You now have a basic Gentoo system running, from here you can install a web
server, a DLNA server, or whatever you want.

