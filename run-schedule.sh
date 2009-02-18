#!/bin/bash

# HOWTO RUN
# From the /var/wordisms/www directory
#  nohup ./run-schedule.sh > ~/run-schedule1.sh.log &
echo "Running..."
while true; do
    echo "Launching..."
    python /var/wordisms/www/schedule.py
    sleep 5
done
echo "Done."