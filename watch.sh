#/bin/bash

SEARCH=$(ps | egrep '((\w|\.|\d|\-)*\/)+Python ((\w|\.|\d|\-)*\/)+handler.py' | egrep -o '^\d{1,6}')
if [ ${SEARCH:--1} -lt 0 ]
then
	(python3 ~/PycharmProjects/weather-bot/src/handler.py &  > /dev/null) 
fi

while :
do 
	SEARCH=$(ps | egrep '((\w|\.|\d|\-)*\/)+Python ((\w|\.|\d|\-)*\/)+handler.py' | egrep -o '^\d{1,6}')
	if [ ${SEARCH:-0} -lt 1 ]
	then
		echo '(x) - resetting'
		python3 ~/PycharmProjects/weather-bot/src/handler.py & 
	fi
	sleep $1
done