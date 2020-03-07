#!/bin/bash
screen -XS robotServer quit
sleep 1
screen -md -S robotServer sudo python3 /home/pi/testing/robotServer.py
