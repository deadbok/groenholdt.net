author: ObliVion
date: 2015-02-14 16:57
slug: OpenWRT-unbrick-medion-OX820-based-NAS
tags: OpenWRT, NAS, Medion MD86517, unbrick
title: Unbricking the Medion OX820 based NAS running OpenWRT 
type: post
template: post
status: hidden


tftp.
-----

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

Unbricking with tftp.
---------------------

 + Build OpenWRT with initramfs support compressed with xz.
 + Set up a tftp server, serving ”’openwrt-oxnas-stg212-fit-uImage-initramfs.itb”’

On the device, interrupt uboot, then:

	tftp 64000000 openwrt-oxnas-stg212-fit-uImage-initramfs.itb bootm
