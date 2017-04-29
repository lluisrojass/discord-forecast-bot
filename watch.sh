#/bin/bash

# suppress terminated messages
(python3 ~/PycharmProjects/weather-bot/src/handler.py &  > /dev/null) 

while :
do 
	# check if running
	RUNPID=$(ps | egrep '((\w|\.|\d|\-)*\/)+Python ((\w|\.|\d|\-)*\/)+handler.py' | egrep -o '^\d{1,6} ')
	if [ ${RUNPID:-1} -gt 1 ]
	then
		echo '(✓) - running'
	else 
		echo '(x) - resetting'
		python3 ~/PycharmProjects/weather-bot/src/handler.py & 
	fi
	sleep $1
done