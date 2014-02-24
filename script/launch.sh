#!/bin/bash

# Path declarations
SRC_PATH="../src/"

ICOMM_PATH=$SRC_PATH"IComm/"
TRADUCTOR_PATH=$SRC_PATH"traducteur/"

ECHO_PATH=$TRADUCTOR_PATH"echoServer.py"
FAKEJ_PATH=$TRADUCTOR_PATH"fakeJerome.py"
LAUNCHME_PATH=$TRADUCTOR_PATH"launchMe.py"

CONFIG_PATH=$ICOMM_PATH"server/config.json"

LAUNCH_PATH=$ICOMM_PATH"launch.py"
RUNSERVER_PATH=$ICOMM_PATH"runserver.py"

if [ "$1" = "-j" ] # If true Jerome launching
then
		sed -i "s/\"platforme\":.*/\"platforme\":\"134.214.106.23\",/" $CONFIG_PATH
		sed -i "s/\"platformePort\":.*/\"platformePort\":5000,/" $CONFIG_PATH
else
		sed -i "s/\"platforme\":.*/\"platforme\":\"127.0.0.1\",/" $CONFIG_PATH
		sed -i "s/\"platformePort\":.*/\"platformePort\":1515,/" $CONFIG_PATH
		if [[ $2 -eq 2 ]]	# If a terminal is precised
		then
		 	$2 -hold -e python $ECHO_PATH &
		 	$2 -hold -e python $FAKEJ_PATH &
		else	# If no terminal is precised, use xterminal
			xterm -hold -e python $ECHO_PATH &
			xterm -hold -e python $FAKEJ_PATH &
	 	fi
fi

python $LAUNCH_PATH