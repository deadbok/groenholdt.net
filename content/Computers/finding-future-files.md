author: ObliVion
date: 2016-02-10 18:33
tags: unix, file, future
title: Finding future files
type: post
template: post

Sometimes you end up with a system having files modified in the future.
At one time this happened to my Raspberry Pi, who was set up to sent me
an email when something was wrong. After a friendly reminder every hour,
I set out to find the files, and change their date to something sane.

Using `find`, this give a list of the files:

	find . -newermt "5 days" -ls
	
Combine it with touch , to change the date to the current.

	find . -newermt "5 days" -ls -exec touch -c {} \;
	
