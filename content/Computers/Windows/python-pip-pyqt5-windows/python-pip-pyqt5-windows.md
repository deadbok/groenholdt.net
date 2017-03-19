author: ObliVion
date: 2017-03-19 21:44
slug: python-pip-pyqt5-windows
tags: Windows, Python, pip, PyQT5
title: Installing PyQT5 for use in Python 3 on Windows 10
type: post
template: post


From fellow classmates I have been asked to show how to install PyQT5 on a
Windows 10 system for use in Python 3 in our programming classes. Coming from
Linux I initially just said "Well, install it" but it turns out to be a little
more involved than that. The [PyQT](https://riverbankcomputing.com/software/pyqt/intro)
homepage, seems to no longer have Windows binaries available for download, there
are other sources, but I wanted to find something that was as reliable as
installing the package on a Linux system.

There are probably easier ways of achieving this, but this is the method I
settled on:

**Find your Python 3 directory**

Python will install itself under your user directory. My Windows user name is
`olebole`, and Python 3.6 is at:

    C:\Users\olebole\AppData\Local\Programs\Python\Python36

When using the Windows Explorer you will have to enable showing hidden folders
and files to see the `AppData` folder in your home directory.

You need to find your Python location since this is where `pip` is installed. [Pip](https://packaging.python.org/key_projects/#pip) is used to install packages from [PyPI - the Python Package Index](https://pypi.python.org/pypi).

**Install PyQT5**
!{Installing on my current computer in running Windows 10}($LOCALURL/python-pip-pyqt5-windows.png)
Now that you have your Python installation path, proceed to start a command
shell (Win+R, cmd, Enter) and change into the `Scripts` directory in the Python
installation directory and use `pip.exe` to install PyQT5.

    cd c:\Users\oblivion\AppData\Local\Programs\Python\Python36\Scripts

    pip install PyQT5

**Setting the PATH**

If you expect on doing this a lot it would be a good idea to add the path of
pip.exe to the PATH environment variable. I leave this as an exercise to the
reader, while I hurry back to my trusted terminal window.
