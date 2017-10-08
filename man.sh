#!/bin/bash
if [ "$EUID" -ne 0 ]
	then echo "Please run as root"
	exit
fi
if [ ! -d /usr/local/share/man/man1 ]; then
	mkdir /usr/local/share/man/man1
fi
	python ./setup.py build_manpage 
	cp coala.1 /usr/local/share/man/man1/
	mandb 

