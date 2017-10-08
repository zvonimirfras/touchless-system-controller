#!/bin/sh

# leapd keeps segfaulting so bring it back up every time it dies, phoenix style
while true; do
    leapd
    sleep 0.5  # give the opportunity to kill the loop and exit the script
done
