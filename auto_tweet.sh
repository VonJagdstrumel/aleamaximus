#!/bin/bash

set -x
while :; do
    random_nr=$(od -An -td -N3 /dev/urandom)
    # wait between 6 and 24 hours
    sleep $(($random_nr % 64800 + 21600))
    curr_hour=$(date +%-H)
    
    # not between midnight and 7
    if (( $curr_hour > 6 )) && (( $curr_hour <= 23 )); then
        ./tweet.py $(cat "$1") < "$2"
        sed -i 1d "$2"
        date
    fi
done
