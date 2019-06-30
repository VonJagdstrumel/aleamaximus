#!/usr/bin/env bash

DISCORD_SESSION_ID=
DISCORD_CHANNEL_ID=
TWITTER_CONSUMER_TOKEN=
TWITTER_CONSUMER_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_SECRET=

mkdir -p user

if [ ! -d venv ]; then
    python3 -mvenv venv
fi

. venv/bin/activate

if [ ! -f user/whitelist.txt ]; then
    touch user/whitelist.txt
fi

if [ ! -f user/discord.db ]; then
    sqlite3 user/discord.db < discord.sql
    ./fetch.py -t $DISCORD_SESSION_ID -c $DISCORD_CHANNEL_ID -d user/discord.db
    ./clean.py user/discord.db < user/whitelist.txt
fi

if [[ "$TWITTER_CONSUMER_TOKEN$TWITTER_CONSUMER_SECRET" && ! "$TWITTER_ACCESS_TOKEN$TWITTER_ACCESS_SECRET" ]]; then
    ./tweet.py -t $TWITTER_CONSUMER_TOKEN -c $TWITTER_CONSUMER_SECRET
elif [ -f user/generated.txt ]; then
    ./tweet.py -t $TWITTER_CONSUMER_TOKEN -c $TWITTER_CONSUMER_SECRET -a $TWITTER_ACCESS_TOKEN -s $TWITTER_ACCESS_SECRET < user/generated.txt
    sed -i 1d user/generated.txt
else
    sqlite3 user/discord.db 'SELECT content FROM clean_message' | ./generate.py 100 > user/temp_generated.txt
fi