#!/bin/bash
while (true)
do
	inotifywait -q -e modify /home/pete/Documents/Code/wacl_Lattepanda
	pkill -9 -f liveplotting
	python3 /home/pete/Documents/Code/wacl_Lattepanda/liveplotting.py
done
