#!/bin/bash
if [ "$EUID" -ne 0 ]
	then echo "Please run as root"
	exit
fi
if [ -f /usr/local/share/man/coala ]; then
	mkdir /usr/local/share/man/coala
fi
	echo "Coala man is installing..."
	python ./setup.py build_manpage > /dev/null
	cp coala.1 /usr/local/share/man/coala/
	mandb > /dev/null
	rm coala.1 > /dev/null
