author: ObliVion
date: 2014-08-06 20:00
tags: Gentoo, NAS, Medion MD86517, kernel
title: Medion NAS native kernel compile
type: post
template: post

I did not compile in netfilter in the cross compiled kernel I made in the 
[previous post]($LOCALURL/medion-0x820-based-nas/medion-ox820-based-nas.html), so I had to recompile. Here is how to compile and install the 
kernel natively on the NAS.

Install mkimage.
================

The package ``u-boot-tools`` is needed to get the ``mkimage`` command to make an U-Boot kernel image.

    emerge u-boot-tools

Compile the kernel.
===================

Go to the sources and reconfigure them using menuconfig.
    
    cd /usr/src/linux
    make menuconfig
  
Compile kernel.

    make zImage ox820-pogoplug-pro.dtb
    
Compile and install modules.

    make modules
    make modules_install

Create the kernel image.

    cat arch/arm/boot/zImage arch/arm/boot/dts/ox820-pogoplug-pro.dtb > arch/arm/boot/zImage.fdt
    scripts/mkuboot.sh -A arm -O linux -C none -T kernel -a 0x60008000 -e 0x60008000 -n 'Linux-3.11.1+' -d arch/arm/boot/zImage.fdt arch/arm/boot/uImage

Write the image to the disk.
============================

Edit the disk_create script to change the target drive in the variable ``disk`` to ``/dev/sda``.

Integrate the new kernel into WarheadsSE's tool.

    cd /usr/src/disk_create
    cp /usr/src/linux/arch/arm/boot/uImage uImages/gentoo

Write the image.
    
    ./disk_create

Done.
====

Happy hacking.