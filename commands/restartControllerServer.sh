#!/bin/bash
screen -XS controllerServer quit
sleep 5
screen -md -S controllerServer sudo python3 /home/pi/working/client.py