author: ObliVion
date: 2015-08-10 03:25
tags: gentoo, portage
title: Regenerating all manifest in the portage tree
template: post


**The first thing to do if you have manifest errors, is to find out why!
Do not blindly recreate your manifests.**

After several syncs emerge kept complaining about missing digests for a
huge amount of ebuilds on the system. I guess this shuold solve itself 
at some future sync, but in the meantime I couldn't merge anything 
because of the mising digest, so I digged around and crafted this command
to rebuild all digests/manifests in the portage tree.

	find /usr/portage -type d -exec sh -c 'find "{}" -maxdepth 1 -type f -name '*.ebuild'| sort | head -n 1| xargs -r -I --  sudo ebuild -- manifest' ";"

The command finds the first .ebuild file in every subdirectory of 
```/usr/portage``` and runs ```sudo ebuld minifest``` on it.

...And why you shouldn't.
=========================

```manifest``` files contain digest and file size of every source tarball
that Gentoo uses to build your system. If every manifest is regenerated
locally, maliciously changed source tarballs (and we just don not know
for sure if there are any, do we) on you computer will get a valid 
manifest file, making it possible to install it.
