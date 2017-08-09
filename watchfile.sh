#!/bin/bash

while inotifywait -m -e modify /home/pete/Documents/Code/wacl_Lattepanda
do
	pkill -9 -f liveplotting
	python3 /home/pete/Documents/Code/wacl_Lattepanda/liveplotting.py
done
