author: ObliVion
date: 2018-05-03 01:03
tags: gentoo, portage, distcc, libunistring
title: guile, gnutls and others fails to find distc compiled libunistring
template: post


I have had this error a couple of times, and each time it took a while to figure
out the problem.

## Symptom

Guile, gnutls or some other package fails to find libunistring during the
configure stage of emerge.

## Sollution

Compile libunistring locally (belt and suspenders version):

    FEATURES="-ditcc -distcc-pump" MAKEOPTS="-j1" emerge -j1 libunistring
