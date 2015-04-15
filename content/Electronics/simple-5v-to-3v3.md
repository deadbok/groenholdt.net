author: ObliVion
date: 2015-04-15 22:52
tags: Final design, vreg, 5V, 3.3V
title: Simple discrete 5V to 3.3V voltage regulator
type: post
template: post

I wanted to start working with my [ESP8266](http://www.esp8266.com/)
nad needed a 3.3V regulator to get enough current. I had ordered some 
1117 regulators, but went looking through what I had laying about, and
"created" this simple circuit.

It is not very efficient, and would benefit from a darlington in place 
of Q1, but it gets the job done with enough current for the ESP8266. If 
the output voltage is just a tad to large, try replacing D1 with a 
Schottky type.

!{Schematic}($LOCALURL/5vto3v3.png)
<br style="clear: both;" />




