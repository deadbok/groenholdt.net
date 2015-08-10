author: ObliVion
date: 2015-08-08 22:39
status: hidden
tags: debian, jasper, voice control
title: Jasper on Debian
template: post

Jasper on Debian
================

	sudo apt-get install python-pip
	
	sudo pip install --upgrade setuptools
	sudo apt-get install python-dev liblapack-dev python-pyaudio espeak pocketsphinx python-pocketsphinx portaudio19-dev
	sudo pip install --allow-all-external --allow-unverified PyAudio PyAudio
	sudo pip install --upgrade -r client/requirements.txt
	
	sudo apt-get install subversion autoconf libtool automake gfortran g++
	svn co https://svn.code.sf.net/p/cmusphinx/code/trunk/cmuclmtk/
	cd cmuclmtk/
	
If you do not want to clutter your global /usr, remove ```--prefix=/usr```.
CMUCLMTK will be installed in /usr/local, and you need to adjust the rest
accordingly.
	
	./autogen.sh --prefix=/usr
	make
	sudo make install
	
	sudo su -c "echo 'deb http://ftp.debian.org/debian experimental main contrib non-free' > /etc/apt/sources.list.d/experimental.list"

Comment out the corresponding line in ```/etc/apt/sources.lst```.

	sudo apt-get update
	sudo apt-get -t experimental install phonetisaurus m2m-aligner mitlm libfst-tools
	wget http://phonetisaurus.googlecode.com/files/g014b2b.tgz
	tar xvzf g014b2b.tgz 
	cd g014b2b
	./compile-fst.sh

Add Text-To-Speech software
	
	sudo apt-get install libttspico-utils
	
Change to into your Jasper directory.

	cd client
	python populate.py
	
Edit ```~/.jasper/profile.yml``` and add

	tts_engine: pico-tts
	stt_engine: sphinx
	
	pocketsphinx:
		fst_model: '/install/g014b2b/g014b2b.fst'                        #optional
		hmm_dir: '/usr/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k' #optional

	
