#!/bin/sh

# leapd keeps segfaulting so bring it back up every time it dies, phoenix style
while true; do
    leapd
done
