author: ObliVion
date: 2016-15-09 20:44
tags: rsync, sync, linux, windows, file transfer
title: rsync --info option
type: post
template: post

Since I first learned of [rsync](https://rsync.samba.org/), copying files
have not been the same. If you do not know `rsync`, you should read up
on it now.

Though I like `rsync` I have always been a little bothered that there
was seemingly no way of forcing `rsync` to count the total number of
files before transferring them, thus making the --progress option
partially useless. This time I did some research, and found that if
your `rsync` is newer than version 3.1.0 there is an `--info` option.

From the [rsync manual page](https://download.samba.org/pub/rsync/rsync.html):

	--info=FLAGS
    This option lets you have fine-grained control over the information output you want to see. An individual flag name may be followed by a level number, with 0 meaning to silence that output, 1 being the default output level, and higher numbers increasing the output of that flag (for those that support higher levels). Use --info=help to see all the available flag names, what they output, and what flag names are added for each increase in the verbose level. Some examples:

        rsync -a --info=progress2 src/ dest/
        rsync -avv --info=stats2,misc1,flist0 src/ dest/ 

    Note that --info=name's output is affected by the --out-format and --itemize-changes (-i) options. See those options for more information on what is output and when.

    This option was added to 3.1.0, so an older rsync on the server side might reject your attempts at fine-grained control (if one or more flags needed to be send to the server and the server was too old to understand them). See also the "max verbosity" caveat above when dealing with a daemon. 
    
With the `--info=progress2` i get the following kind of output:

	receiving incremental file list
				0   0%    0.00kB/s    0:00:00 (xfr#0, ir-chk=1001/71529)
	Documents/development/projects/C/linux/cdcat/src/gcdCat/src/.deps/
				0   0%    0.00kB/s    0:00:00 (xfr#0, ir-chk=1000/71612)
	Documents/development/projects/C/linux/cdcat/src/gcdCat/src/CVS/
				0   0%    0.00kB/s    0:00:00 (xfr#0, ir-chk=1000/73443)
	Documents/ebooks/Humble bundle/
				0   0%    0.00kB/s    0:00:00 (xfr#0, ir-chk=1014/73485)
				
Which seem what I have wished for.
