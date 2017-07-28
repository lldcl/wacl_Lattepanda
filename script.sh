#!/bin/bash
{

script_prev=$(pgrep script)
readarray -t lines < <(echo "$script_prev")
if [ -n "${lines[1]}" ]
then
	kill -9 "${lines[0]}"
	pkill -9 python
	echo "Killing previous script..."
fi

pkill -9 python

DISPLAY=:0
export DISPLAY
/home/pete/Documents

while(true)
do
	running1=$(ps aux |grep [US]B_poll_test1.py)
	running2=$(ps aux |grep [US]B_poll_test2.py)
	running3=$(ps aux |grep [li]veplotting.py)
	if [ \( -n "$running1" \) -a \( -n "$running2" \) -a \( -n "$running3" \) ]
	then
		echo "recording"
		sleep 20

	elif [ -z "$running1" ]
	then
		echo "Starting Arduino 1"
		python3 /home/pete/Documents/Code/USB_poll_test1.py& 
		sleep 2
	elif [ -z "$running2" ]
	then
		echo "Starting Arduino 2"
		python3 /home/pete/Documents/Code/USB_poll_test2.py&
		sleep 2
	elif [ \( -n "$running1" \) -a \( -z "$running3" \) ]
	then
		echo "Starting Live plotting"
		python3 /home/pete/Documents/Code/liveplotting.py&
	fi
done
} > logfile


