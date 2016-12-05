author: ObliVion
date: 2016-11-29 20:05
tags: Linux, console, beep, happy birthday
title: Happy birthday with beep
type: post
template: post


I used the following beep sequence to remotely play "Happy birthday" for
a friend at his office through VPN.

	beep -f 261.6 -n -f 261.6 -n -f 293.7 -n -f 261.6 -n -f 349.2 \
	     -n -l 500 -f 329.6 -n -f 1 -n -f 261.6 -n -f 261.6 -n -f 293.7 \
	     -n -f 261.6 -n -f 392.0 -n -l 500 -f 349.2 -n -f 1 -n -f 261.6 \
	     -n -f 261.6 -n -f 523.2 -n -f 440.0 -n -f 349.2 -n -f 329.6 \
	     -l 200 -n -f 293.7 -n -f 1 -n -f 523.2 -n -f 523.2 -n -f 440.0 \
	     -n -f 349.2 -n -f 392.0 -n -f 349.2
