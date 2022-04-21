#!/bin/bash
# Usage:
# source init_script.sh

if [ ! -d "pyvenv" ]; then

	echo "Virtual Environment not found. Creating .."
	#virtualenv pyvenv           # Python2.7
	#python3 -m venv pyvenv     # Python3.6
	virtualenv -p /usr/bin/python3.8 pyvenv    #Create virtual env with Python3.8
	source pyvenv/bin/activate

	if [ $VIRTUALENV != "" ]; then
	 echo "Virtual Env Activated"
	 pip install -r src/requirements.txt
	fi

fi

